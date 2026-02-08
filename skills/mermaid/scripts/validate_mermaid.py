#!/usr/bin/env python3
"""
Mermaid 图表验证工具

功能：
1. 自动检测并安装 @mermaid-js/mermaid-cli
2. 验证 Mermaid 语法正确性（实际渲染测试）
3. 分析图表复杂度
4. 评估视觉质量并提供评分
5. 提供优化建议

    使用方法：
        python3 validate_mermaid.py <diagram.md> [--verbose]

    返回码：
        0 - 验证通过
        1 - 验证失败或错误
"""

import argparse
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, Tuple


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """将十六进制颜色转换为RGB"""
    hex_color = hex_color.lstrip("#")
    rgb_values = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    return (rgb_values[0], rgb_values[1], rgb_values[2])


def get_luminance(rgb: Tuple[int, int, int]) -> float:
    """计算颜色的亮度（WCAG 2.1 标准）"""
    r, g, b = [x / 255.0 for x in rgb]

    # 转换为线性RGB
    r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
    g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
    b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4

    # 计算亮度
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def get_contrast_ratio(rgb1: Tuple[int, int, int], rgb2: Tuple[int, int, int]) -> float:
    """计算两个颜色的对比度（WCAG 2.1 标准）"""
    l1 = get_luminance(rgb1)
    l2 = get_luminance(rgb2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


class MermaidValidator:
    """Mermaid 图表验证器"""

    def __init__(self):
        self.mmdc_cmd = None
        self.verbose = False
        self.auto_install = False
        self.strict_mode = False  # 严格模式（推荐标准）

    # ========== CLI 检测和安装 ==========

    def check_and_install_cli(self) -> bool:
        """检测并安装 mermaid-cli"""
        if self._check_mmdc_installed():
            return True

        print("📦 未检测到 @mermaid-js/mermaid-cli，准备安装...")
        print("   提示：需要 Node.js 环境")

        # 检查 Node.js
        if not self._check_node_installed():
            print("❌ 未检测到 Node.js，请先安装 Node.js")
            print("   安装方法：https://nodejs.org/")
            return False

        # 自动安装模式跳过确认
        if not self.auto_install:
            try:
                response = input("是否自动安装? [Y/n]: ").strip().lower()
                if response in ["n", "no"]:
                    print("❌ 验证需要 mermaid-cli，退出")
                    return False
            except EOFError:
                pass

        return self._install_mmdc()

    def _check_node_installed(self) -> bool:
        """检查 Node.js 是否已安装"""
        try:
            result = subprocess.run(
                ["node", "--version"], capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"✅ 检测到 Node.js: {version}")
                return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        return False

    def _check_mmdc_installed(self) -> bool:
        """检查 mmdc 是否已安装"""
        # 方式1：检查全局安装
        if shutil.which("mmdc"):
            self.mmdc_cmd = ["mmdc"]
            try:
                result = subprocess.run(
                    ["mmdc", "--version"], capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    print(f"✅ 检测到 mermaid-cli: {result.stdout.strip()}")
                    return True
            except (FileNotFoundError, subprocess.TimeoutExpired):
                pass

        # 方式2：使用 npx
        try:
            result = subprocess.run(
                ["npx", "-y", "@mermaid-js/mermaid-cli", "--version"],
                capture_output=True,
                text=True,
                timeout=60,
            )
            if result.returncode == 0:
                self.mmdc_cmd = ["npx", "-y", "@mermaid-js/mermaid-cli"]
                print(f"✅ 检测到 mermaid-cli (via npx): {result.stdout.strip()}")
                return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        return False

    def _install_mmdc(self) -> bool:
        """安装 mermaid-cli"""
        print("正在安装 @mermaid-js/mermaid-cli...")
        try:
            subprocess.run(
                ["npm", "install", "-g", "@mermaid-js/mermaid-cli"],
                check=True,
                timeout=300,
            )
            print("✅ 安装成功！")
            return self._check_mmdc_installed()
        except subprocess.CalledProcessError as e:
            print(f"❌ 安装失败：{e}")
            print("   请手动运行：npm install -g @mermaid-js/mermaid-cli")
            return False
        except subprocess.TimeoutExpired:
            print("❌ 安装超时，请检查网络连接")
            return False

    # ========== 验证主流程 ==========

    def validate_file(
        self, filepath: str, verbose: bool = False
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        验证 Mermaid 文件

        Args:
            filepath: 文件路径
            verbose: 是否输出详细信息

        Returns:
            (是否通过, 详细结果)
        """
        self.verbose = verbose

        # 读取文件
        try:
            content = Path(filepath).read_text(encoding="utf-8")
        except FileNotFoundError:
            return False, {"error": f"文件不存在: {filepath}"}
        except Exception as e:
            return False, {"error": f"读取文件失败: {e}"}

        # 1. 语法验证（实际渲染）
        # 确保使用绝对路径，因为 _validate_syntax 会在临时目录中运行 mmdc
        abs_filepath = os.path.abspath(filepath)
        syntax_ok, syntax_msg = self._validate_syntax(abs_filepath)

        # 2. 主题兼容性检查
        theme_check = self._evaluate_theme_compatibility(content)

        # 3. 复杂度分析
        complexity = self._analyze_complexity(content)

        # 4. 视觉质量评估
        visual = self._evaluate_visual_quality(content, complexity)
        visual["theme_check"] = theme_check  # 添加主题检查结果

        # 5. 最佳实践检查
        best_practices = self._check_best_practices(content)

        # 应用最佳实践扣分
        if "penalties" in best_practices:
            visual["score"] -= best_practices["penalties"]

        # 6. 汇总结果
        result = {
            "syntax": {"passed": syntax_ok, "message": syntax_msg},
            "complexity": complexity,
            "visual": visual,
            "best_practices": best_practices,
        }

        # 判断是否通过
        passed = syntax_ok and visual["score"] >= 60

        # 输出报告
        self._print_report(result, passed)

        return passed, result

    # ========== 语法验证 ==========

    def _validate_syntax(self, filepath: str) -> Tuple[bool, str]:
        """通过实际渲染验证语法"""
        if not self.mmdc_cmd:
            return False, "mermaid-cli 未安装"

        with tempfile.TemporaryDirectory() as tmpdir:
            output = os.path.join(tmpdir, "output.svg")

            try:
                cmd = self.mmdc_cmd + ["-i", filepath, "-o", output]

                # Verbose 模式：打印详细信息
                if self.verbose:
                    print(f"   [调试] mmdc 命令: {' '.join(cmd)}")
                    print(f"   [调试] 输入文件: {filepath}")
                    print(f"   [调试] 输出文件: {output}")

                result = subprocess.run(
                    cmd, capture_output=True, text=True, timeout=60, cwd=tmpdir
                )

                # Verbose 模式：打印执行结果
                if self.verbose:
                    print(f"   [调试] 返回码: {result.returncode}")
                    print(
                        f"   [调试] stdout: {result.stdout[:200] if result.stdout else '(空)'}"
                    )
                    print(
                        f"   [调试] stderr: {result.stderr[:200] if result.stderr else '(空)'}"
                    )

                # 动态查找生成的 SVG 文件
                output_files = glob.glob(os.path.join(tmpdir, "output*.svg"))

                if self.verbose:
                    print(f"   [调试] 找到的输出文件: {len(output_files)}个")
                    for f in output_files:
                        print(f"     - {f}")

                # 判断渲染结果
                if result.returncode == 0 and output_files:
                    return True, "语法正确，渲染成功"
                else:
                    # 改进错误信息捕获
                    error_parts = []
                    if result.returncode != 0:
                        error_parts.append(f"退出码: {result.returncode}")
                    if result.stderr:
                        error_parts.append(f"错误: {result.stderr}")
                    if result.stdout:
                        error_parts.append(f"输出: {result.stdout[:100]}")

                    error_msg = " | ".join(error_parts) if error_parts else "未知错误"

                    # 提取关键错误信息
                    if "Parse error" in error_msg:
                        return False, f"语法解析错误：{error_msg[:200]}"
                    return False, f"渲染失败：{error_msg[:200]}"

            except subprocess.TimeoutExpired:
                return False, "渲染超时（可能图表过于复杂）"
            except Exception as e:
                return False, f"验证错误：{str(e)}"

    # ========== 复杂度分析 ==========

    def _analyze_complexity(self, content: str) -> Dict[str, Any]:
        """分析图表复杂度"""
        # 检测图表类型
        diagram_type = self._detect_diagram_type(content)

        # 统计节点数（不同图表类型使用不同规则）
        nodes = self._count_nodes(content, diagram_type)

        # 统计 subgraph 数量（层次）
        subgraphs = len(re.findall(r"\bsubgraph\b", content, re.IGNORECASE))
        depth = subgraphs + 1 if subgraphs > 0 else 1

        # 统计连接线
        connection_patterns = [
            r"-->",  # 箭头
            r"---",  # 实线
            r"-\.-",  # 虚线
            r"==>",  # 粗箭头
            r"->>",  # 异步箭头
            r"-->>",  # 虚线异步
        ]
        connections = sum(len(re.findall(p, content)) for p in connection_patterns)

        # 分级标准
        recommended_nodes = 20
        recommended_depth = 5
        maximum_nodes = 50
        maximum_depth = 6

        return {
            "type": diagram_type,
            "nodes": nodes,
            "depth": depth,
            "subgraphs": subgraphs,
            "connections": connections,
            # 推荐标准（严格模式）
            "recommended_nodes": recommended_nodes,
            "recommended_depth": recommended_depth,
            "nodes_ok_recommended": nodes < recommended_nodes,
            "depth_ok_recommended": depth < recommended_depth,
            # 最小要求（默认模式）
            "maximum_nodes": maximum_nodes,
            "maximum_depth": maximum_depth,
            "nodes_ok_maximum": nodes < maximum_nodes,
            "depth_ok_maximum": depth < maximum_depth,
            # 兼容性（保留旧字段）
            "nodes_ok": nodes < maximum_nodes,
            "depth_ok": depth < maximum_depth,
        }

    def _detect_diagram_type(self, content: str) -> str:
        """检测图表类型"""
        content_lower = content.lower()

        type_patterns = [
            (r"\bflowchart\b", "Flowchart"),
            (r"\bgraph\b", "Flowchart (legacy)"),
            (r"\bsequencediagram\b", "Sequence Diagram"),
            (r"\bclassdiagram\b", "Class Diagram"),
            (r"\bstatediagram", "State Diagram"),
            (r"\berdiagram\b", "ER Diagram"),
            (r"\bgantt\b", "Gantt"),
            (r"\bpie\b", "Pie Chart"),
            (r"\bmindmap\b", "Mindmap"),
            (r"\btimeline\b", "Timeline"),
            (r"\barchitecture", "Architecture"),
            (r"\bkanban\b", "Kanban"),
            (r"\bblock-beta\b", "Block Diagram"),
        ]

        for pattern, name in type_patterns:
            if re.search(pattern, content_lower):
                return name

        return "Unknown"

    def _count_nodes(self, content: str, diagram_type: str) -> int:
        """统计节点数量"""
        nodes = set()

        if "Flowchart" in diagram_type:
            # 匹配各种节点定义
            patterns = [
                r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\[",  # A[label]
                r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\(",  # A(label)
                r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\{",  # A{label}
                r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\(\[",  # A([label])
                r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\[\[",  # A[[label]]
                r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\[\(",  # A[(label]]
            ]
            for pattern in patterns:
                matches = re.findall(pattern, content)
                nodes.update(matches)

        elif "Sequence" in diagram_type:
            # 匹配参与者
            participants = re.findall(r"\bparticipant\s+(\w+)", content, re.IGNORECASE)
            actors = re.findall(r"\bactor\s+(\w+)", content, re.IGNORECASE)
            nodes.update(participants)
            nodes.update(actors)

        elif "Class" in diagram_type:
            # 匹配类定义
            classes = re.findall(r"\bclass\s+(\w+)", content)
            nodes.update(classes)

        elif "Gantt" in diagram_type:
            # 匹配任务
            tasks = re.findall(r"^\s*[^:\n]+\s*:", content, re.MULTILINE)
            return len(tasks)

        else:
            # 通用节点统计
            generic = re.findall(r"\b([A-Z][A-Za-z0-9_]*)\s*[\[\(\{]", content)
            nodes.update(generic)

        # 排除关键字
        keywords = {
            "subgraph",
            "end",
            "graph",
            "flowchart",
            "direction",
            "style",
            "classDef",
            "click",
            "class",
            "participant",
            "actor",
            "Note",
            "loop",
            "alt",
            "opt",
            "par",
            "critical",
            "break",
        }
        nodes = nodes - keywords

        return len(nodes)

    # ========== 视觉质量评估 ==========

    def _evaluate_theme_compatibility(self, content: str) -> Dict[str, Any]:
        """评估主题与环境的兼容性"""
        result = {
            "has_theme": False,
            "theme": None,
            "theme_type": None,
            "warnings": [],
            "suggestions": [],
        }

        # 检测是否配置了主题（支持多种格式）
        has_init = "%%{init:" in content
        has_config_unix = "---\nconfig:" in content
        has_config_windows = "---\r\nconfig:" in content

        if not (has_init or has_config_unix or has_config_windows):
            result["warnings"].append("未配置主题，使用默认样式")
            result["suggestions"].append(
                "建议配置主题：%%{init: {'theme':'default'}}%%（浅色）或 "
                "%%{init: {'theme':'dark'}}%%（深色）"
            )
            return result

        result["has_theme"] = True

        # 记录主题配置类型
        if has_init:
            result["theme_type"] = "init"
        elif has_config_unix or has_config_windows:
            result["theme_type"] = "frontmatter"

        # 提取主题名称（支持两种格式）
        theme = None

        # 格式1: %%{init: {'theme':'default'}}%%
        if has_init:
            theme_match = re.search(r"'theme'\s*:\s*'([^']+)'", content)
            if theme_match:
                theme = theme_match.group(1)

        # 格式2: ---\nconfig:\n  theme: default
        if (has_config_unix or has_config_windows) and not theme:
            theme_match = re.search(r"theme:\s*([^\s\n]+)", content)
            if theme_match:
                theme = theme_match.group(1)

        if theme:
            result["theme"] = theme

            # 检测 default 主题的兼容性问题
            if theme == "default":
                result["warnings"].append("default主题在深色背景下连接线对比度可能不足")
                result["suggestions"].append(
                    "如果在dark模式编辑器中查看，建议切换到 dark 或 forest 主题"
                )
            elif theme == "dark":
                result["suggestions"].append("dark主题适合深色背景，浅色背景下可能过暗")

        return result

    def _check_color_contrast(self, content: str) -> Dict[str, Any]:
        """检查颜色对比度"""
        result = {"checked": False, "issues": [], "suggestions": []}

        # 查找所有的样式定义
        style_patterns = re.findall(
            r"style\s+(\w+)\s+fill:#([0-9a-fA-F]{6})\s*,\s*stroke:#([0-9a-fA-F]{6})",
            content,
        )

        if not style_patterns:
            return result

        result["checked"] = True

        # 默认文字颜色（根据主题推断）
        has_dark_theme = "'theme':'dark'" in content or "theme: dark" in content
        default_text_rgb = (248, 249, 250) if has_dark_theme else (51, 51, 51)

        low_contrast_nodes = []

        for node_id, fill_hex, stroke_hex in style_patterns:
            fill_rgb = hex_to_rgb(fill_hex)

            # 计算填充色与文字色的对比度
            contrast = get_contrast_ratio(fill_rgb, default_text_rgb)

            # WCAG AA 标准：至少 4.5:1
            if contrast < 4.5:
                low_contrast_nodes.append(
                    {"node": node_id, "fill": fill_hex, "contrast": round(contrast, 2)}
                )

        if low_contrast_nodes:
            result["issues"].append(
                f"发现{len(low_contrast_nodes)}个节点对比度不足（WCAG AA 要求 4.5:1）"
            )
            result["suggestions"].append(
                "建议调整颜色以提升对比度，或使用浅色/深色文字"
            )
        else:
            result["suggestions"].append("✅ 颜色对比度符合WCAG AA标准")

        return result

    def _evaluate_visual_quality(
        self, content: str, complexity: Dict
    ) -> Dict[str, Any]:
        """评估视觉质量"""
        score = 100
        issues = []
        suggestions = []

        # 1. 主题配置检查（-15分）
        theme_check = self._evaluate_theme_compatibility(content)

        if not theme_check["has_theme"]:
            score -= 15
            issues.append("未配置主题，使用默认样式")
            suggestions.append("配置主题：%%{init: {'theme':'default'}}%%")
        else:
            # 添加主题兼容性建议
            if theme_check["warnings"]:
                issues.extend(theme_check["warnings"])
            if theme_check["suggestions"]:
                suggestions.extend(theme_check["suggestions"])

        # 2. 布局方向检查（-10分）
        if "Flowchart" in complexity["type"]:
            has_direction = any(d in content for d in ["TD", "TB", "LR", "RL", "BT"])
            if not has_direction and "graph " not in content.lower():
                score -= 10
                issues.append("Flowchart未明确指定布局方向")
                suggestions.append("明确方向：flowchart TD 或 flowchart LR")

        # 3. 分组使用检查（节点>10时，-20分）
        if complexity["nodes"] > 10 and complexity["subgraphs"] == 0:
            score -= 20
            issues.append(f"节点较多({complexity['nodes']}个)但未使用subgraph分组")
            suggestions.append("使用subgraph提升视觉层次和组织性")

        # 4. 样式定制检查（建议）
        has_style = "style " in content or "classDef " in content
        if complexity["nodes"] > 5 and not has_style:
            suggestions.append("使用style或classDef突出重要节点")

        # 5. 节点形状多样性检查（建议）
        shape_patterns = [
            (r"\[.*?\]", "rectangle"),
            (r"\(.*?\)", "rounded"),
            (r"\{.*?\}", "diamond"),
            (r"\(\[.*?\]\)", "stadium"),
            (r"\[\(.*?\)\]", "cylinder"),
        ]
        shapes_used = sum(1 for p, _ in shape_patterns if re.search(p, content))
        if complexity["nodes"] > 5 and shapes_used == 1:
            suggestions.append("使用不同节点形状区分组件类型")

        # 6. 标签长度检查（-10分）
        recommended_label_length = 10
        maximum_label_length = 25

        labels = re.findall(r"\[(.*?)\]", content)
        long_labels = [
            label
            for label in labels
            if len(label) > recommended_label_length and not label.startswith('"')
        ]
        very_long_labels = [
            label
            for label in labels
            if len(label) > maximum_label_length and not label.startswith('"')
        ]

        if very_long_labels:
            score -= int(min(8, len(very_long_labels) * 1))
            issues.append(
                f"发现{len(very_long_labels)}个标签过长(>{maximum_label_length}字)"
            )
            suggestions.append(f"简化标签，保持<{maximum_label_length}个字符")
        elif long_labels:
            score -= int(min(5, len(long_labels) * 0.5))
            issues.append(
                f"发现{len(long_labels)}个标签较长(>{recommended_label_length}字)"
            )
            suggestions.append(f"简化标签，推荐<{recommended_label_length}个字符")

        # 7. 颜色使用检查（建议）
        has_colors = "fill:" in content or "stroke:" in content
        if has_style and not has_colors:
            suggestions.append("为样式添加颜色以提升视觉效果")

        # 8. 颜色对比度检查
        contrast_check = self._check_color_contrast(content)
        if contrast_check["checked"]:
            # 将对比度检查结果添加到返回值中
            pass  # 将在返回字典时添加

        # 8. 复杂度扣分（分级标准）
        recommended_nodes = complexity.get("recommended_nodes", 20)
        maximum_nodes = complexity.get("maximum_nodes", 50)
        recommended_depth = complexity.get("recommended_depth", 5)
        maximum_depth = complexity.get("maximum_depth", 6)

        if complexity["nodes"] >= 100:
            score -= 15
            issues.append(
                f"节点数过多({complexity['nodes']}个)，建议<{recommended_nodes}"
            )
        elif complexity["nodes"] >= maximum_nodes:
            score -= 10
            issues.append(
                f"节点数较多({complexity['nodes']}个)，建议<{recommended_nodes}（最小<{maximum_nodes}）"
            )

        if complexity["depth"] >= maximum_depth:
            score -= 10
            issues.append(
                f"层次过深({complexity['depth']}层），建议<{recommended_depth}（最小<{maximum_depth}）"
            )

        # 确保分数在0-100之间
        score = max(0, min(100, score))

        return {
            "score": score,
            "grade": self._get_grade(score),
            "issues": issues,
            "suggestions": suggestions,
            "contrast_check": contrast_check,
        }

    def _get_grade(self, score: int) -> str:
        """获取视觉质量等级"""
        if score >= 90:
            return "优秀 ⭐⭐⭐⭐"
        elif score >= 80:
            return "良好 ⭐⭐⭐"
        elif score >= 70:
            return "中等 ⭐⭐⭐"
        elif score >= 60:
            return "及格 ⭐⭐"
        else:
            return "需改进 ⭐"

    # ========== 最佳实践检查 ==========

    def _check_best_practices(self, content: str) -> Dict[str, Any]:
        """检查最佳实践"""
        issues = []
        suggestions = []
        penalties = 0  # 扣分项

        # 1. 检查关键字冲突
        keywords = ["end", "class", "click", "call", "Note", "loop"]
        for kw in keywords:
            # 检查是否用作节点ID（后面跟着节点定义符号）
            if re.search(rf"\b{kw}\s*[\[\(\{{]", content):
                issues.append(f"'{kw}'是保留关键字，建议用引号包裹")

        # 2. 检查使用废弃语法（扣5分）
        if "graph " in content.lower() and "flowchart" not in content.lower():
            issues.append("'graph'已废弃，建议使用'flowchart'")
            suggestions.append("将 'graph' 替换为 'flowchart'")
            penalties += 5

        # 3. 检查特殊字符
        if re.search(r"\[[^\]]*[\(\)\{\}][^\]]*\]", content):
            suggestions.append("标签中包含特殊字符，确保已用引号包裹")

        # 4. 检查空的subgraph
        if re.search(r"subgraph\s+\w+\s*\n\s*end", content):
            issues.append("存在空的subgraph")

        # 5. 检查连接线样式一致性
        arrow_types = []
        if "-->" in content:
            arrow_types.append("-->")
        if "--->" in content:
            arrow_types.append("--->")
        if "==>" in content:
            arrow_types.append("==>")
        if len(arrow_types) > 2:
            suggestions.append("使用了多种箭头样式，确保有意为之")

        return {"issues": issues, "suggestions": suggestions, "penalties": penalties}

    # ========== 报告输出 ==========

    def _print_report(self, result: Dict, passed: bool):
        """打印验证报告"""
        print()
        print("=" * 60)
        print("📊 Mermaid 图表验证报告")
        print("=" * 60)

        # 语法验证
        syntax = result["syntax"]
        if syntax["passed"]:
            print("✅ 语法验证：通过")
        else:
            print("❌ 语法验证：失败")
            print(f"   {syntax['message']}")
            print("=" * 60)
            return

        # 复杂度分析
        complexity = result["complexity"]
        print("\n📈 复杂度分析：")
        print(f"   图表类型：{complexity['type']}")

        # 显示分级标准
        recommended_nodes = complexity.get("recommended_nodes", 20)
        maximum_nodes = complexity.get("maximum_nodes", 50)
        recommended_depth = complexity.get("recommended_depth", 5)
        maximum_depth = complexity.get("maximum_depth", 6)

        # 节点数检查
        if complexity["nodes"] < recommended_nodes:
            print(
                f"   节点数：{complexity['nodes']} ✅ 推荐<{recommended_nodes} / 最小<{maximum_nodes}"
            )
        elif complexity["nodes"] < maximum_nodes:
            print(
                f"   节点数：{complexity['nodes']} ⚠️ 推荐<{recommended_nodes} / 最小<{maximum_nodes}"
            )
        else:
            print(
                f"   节点数：{complexity['nodes']} ❌ 建议<{recommended_nodes} / 必须<{maximum_nodes}"
            )

        # 层次深度检查
        if complexity["depth"] < recommended_depth:
            print(
                f"   层次深度：{complexity['depth']} ✅ 推荐<{recommended_depth} / 最小<{maximum_depth}"
            )
        elif complexity["depth"] < maximum_depth:
            print(
                f"   层次深度：{complexity['depth']} ⚠️ 推荐<{recommended_depth} / 最小<{maximum_depth}"
            )
        else:
            print(
                f"   层次深度：{complexity['depth']} ❌ 建议<{recommended_depth} / 必须<{maximum_depth}"
            )

        if complexity["subgraphs"] > 0:
            print(f"   分组数：{complexity['subgraphs']}")
        print(f"   连接线：{complexity['connections']}")

        # 视觉质量
        visual = result["visual"]
        print(f"\n🎨 视觉质量评分：{visual['score']}分 - {visual['grade']}")

        # 主题检查
        if "theme_check" in visual and visual["theme_check"]:
            theme_check = visual["theme_check"]
            if theme_check["theme"]:
                print(f"   当前主题：{theme_check['theme']}")

            if theme_check["warnings"]:
                print("\n⚠️  主题兼容性警告：")
                for warning in theme_check["warnings"]:
                    print(f"   • {warning}")

            if theme_check["suggestions"]:
                print("\n💡 主题切换建议：")
                for suggestion in theme_check["suggestions"]:
                    print(f"   • {suggestion}")

        # 颜色对比度检查
        if "contrast_check" in visual and visual["contrast_check"]:
            contrast_check = visual["contrast_check"]
            if contrast_check["checked"]:
                if contrast_check["issues"]:
                    print("\n⚠️  颜色对比度问题：")
                    for issue in contrast_check["issues"]:
                        print(f"   • {issue}")
                if contrast_check["suggestions"]:
                    print("\n💡 颜色对比度建议：")
                    for suggestion in contrast_check["suggestions"]:
                        print(f"   • {suggestion}")

        if visual["issues"]:
            print("\n⚠️  视觉问题：")
            for issue in visual["issues"]:
                print(f"   • {issue}")

        if visual["suggestions"]:
            # 避免重复显示主题建议
            non_theme_suggestions = [
                s
                for s in visual["suggestions"]
                if "theme:" not in s.lower() and "主题" not in s
            ]
            if non_theme_suggestions:
                print("\n💡 视觉优化建议：")
                for suggestion in non_theme_suggestions:
                    print(f"   • {suggestion}")

        # 最佳实践
        bp = result["best_practices"]
        if bp["issues"]:
            print("\n⚠️ 最佳实践问题：")
            for issue in bp["issues"]:
                print(f"   • {issue}")

        # 总结
        print()
        print("=" * 60)
        if passed:
            if visual["score"] >= 80:
                print("✅ 验证通过 - 图表质量良好")
            else:
                print("✅ 验证通过 - 建议优化视觉效果")
        else:
            print("❌ 验证未通过 - 请修复问题后重新验证")
        print("=" * 60)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Mermaid 图表验证工具")
    parser.add_argument("filepath", help="Mermaid 图表文件路径")
    parser.add_argument("-v", "--verbose", action="store_true", help="显示详细信息")
    parser.add_argument(
        "-s",
        "--strict",
        action="store_true",
        help="严格模式（使用推荐标准：节点<20, 深度<5, 标签<10字）",
    )
    parser.add_argument(
        "-y",
        "--auto-install",
        action="store_true",
        help="自动安装依赖（不询问）",
    )
    parser.add_argument(
        "--move-to",
        metavar="PATH",
        help="验证通过后将文件移动到指定路径",
    )

    args = parser.parse_args()

    # 检查文件
    if not os.path.exists(args.filepath):
        print(f"❌ 文件不存在: {args.filepath}")
        sys.exit(1)

    # 创建验证器
    validator = MermaidValidator()
    validator.auto_install = args.auto_install
    validator.strict_mode = args.strict

    # 检查并安装 CLI
    if not validator.check_and_install_cli():
        sys.exit(1)

    # 执行验证
    passed, _ = validator.validate_file(args.filepath, args.verbose)

    # 验证通过后移动文件
    if passed and args.move_to:
        try:
            # 确保目标目录存在
            target_dir = os.path.dirname(args.move_to)
            if target_dir and not os.path.exists(target_dir):
                os.makedirs(target_dir, exist_ok=True)

            shutil.move(args.filepath, args.move_to)
            if args.verbose:
                print(f"   [移动] 文件已移动到: {args.move_to}")
        except Exception as e:
            print(f"❌ 移动文件失败: {e}")
            sys.exit(1)

    # 返回状态码
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
