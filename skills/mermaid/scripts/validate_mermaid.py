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
        self.content_cache = None  # 缓存文件内容用于错误定位

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
        # 缓存文件内容用于错误解析
        self.content_cache = content
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

    # ========== 错误解析与格式化 ==========

    def _parse_mermaid_error(self, error_msg: str, content: str) -> Dict[str, Any]:
        """
        解析 mermaid-cli 错误信息，提取行号、上下文、错误类型和修复建议

        Args:
            error_msg: 错误信息
            content: 文件内容

        Returns:
            包含错误详细信息的字典
        """
        result = {
            "line_number": None,
            "context_before": [],
            "error_line": None,
            "context_after": [],
            "error_type": None,
            "error_message": error_msg,
            "suggestion": None,
        }

        # 尝试多种错误格式提取行号
        line_patterns = [
            r"line (\d+)",  # 标准格式
            r"at line (\d+)",  # 带前缀
            r":(\d+):",  # 冒号格式
            r"position (\d+)",  # 位置格式
        ]

        for pattern in line_patterns:
            match = re.search(pattern, error_msg, re.IGNORECASE)
            if match:
                result["line_number"] = int(match.group(1))
                break

        # 提取错误类型
        error_type_patterns = [
            (r"Parse error", "syntax"),
            (r"Unexpected token", "syntax"),
            (r"Unexpected end", "syntax"),
            (r"Reserved word", "keyword"),
            (r"is a reserved word", "keyword"),
            (r"Unknown keyword", "keyword"),
            (r"Duplicate ID", "duplicate"),
            (r"Duplicate identifier", "duplicate"),
            (r"Undefined", "reference"),
            (r"not found", "reference"),
        ]

        for pattern, error_type in error_type_patterns:
            if re.search(pattern, error_msg, re.IGNORECASE):
                result["error_type"] = error_type
                break

        # 如果找到行号，提取上下文
        if result["line_number"]:
            lines = content.split("\n")
            line_num = result["line_number"]

            # 上下文行数（前后各2行）
            context_lines = 2

            # 错误行
            if 0 < line_num <= len(lines):
                result["error_line"] = lines[line_num - 1].strip()

                # 前面的行
                start = max(0, line_num - context_lines - 1)
                result["context_before"] = [
                    f"{i + 1}: {lines[i].strip()}"
                    for i in range(start, line_num - 1)
                    if lines[i].strip()
                ]

                # 后面的行
                end = min(len(lines), line_num + context_lines)
                result["context_after"] = [
                    f"{i + 1}: {lines[i].strip()}"
                    for i in range(line_num, end)
                    if lines[i].strip()
                ]

        # 根据错误类型生成建议
        result["suggestion"] = self._get_error_suggestion(result)

        return result

    def _get_error_suggestion(self, error_info: Dict[str, Any]) -> str:
        """根据错误类型提供修复建议"""
        error_type = error_info.get("error_type")
        error_msg = error_info.get("error_message", "")
        error_line = error_info.get("error_line", "")

        # 关键字冲突
        if error_type == "keyword" or "reserved" in error_msg.lower():
            keywords = ["end", "class", "click", "call", "note", "loop", "alt", "opt", "par"]
            for kw in keywords:
                if kw in error_line.lower():
                    return f"'{kw}' 是保留关键字，请用引号包裹（\"{kw}\"）或更换ID名称"

        # 语法错误
        if error_type == "syntax":
            if "-->" in error_line and not error_line.startswith((" ", "\t")):
                return "连接行可能缺少缩进或格式不正确"

            if "[" in error_line and "]" not in error_line:
                return "节点标签缺少闭合的方括号 `]`"

            if "(" in error_line and ")" not in error_line:
                return "节点标签缺少闭合的圆括号 `)`"

            return "检查语法是否正确，特别注意标点符号和括号匹配"

        # 重复ID
        if error_type == "duplicate":
            return "节点ID重复，请确保每个节点ID都是唯一的"

        # 未定义引用
        if error_type == "reference":
            return "引用了未定义的节点，请检查节点ID是否正确"

        # 默认建议
        return "请检查错误行附近的语法和拼写是否正确"

    def _format_error_report(self, error_info: Dict[str, Any]) -> str:
        """格式化友好的错误报告"""
        lines = ["", "❌ 语法验证失败", ""]

        # 错误位置
        if error_info["line_number"]:
            lines.append(f"📍 错误位置：第 {error_info['line_number']} 行")
            lines.append("")

        # 上下文
        if error_info["context_before"] or error_info["error_line"] or error_info["context_after"]:
            lines.append("📄 上下文：")

            for ctx_line in error_info["context_before"]:
                lines.append(f"  {ctx_line}")

            if error_info["error_line"]:
                lines.append(f"  {error_info['line_number']}: {error_info['error_line']}     ← 错误在此行")

            for ctx_line in error_info["context_after"]:
                lines.append(f"  {ctx_line}")

            lines.append("")

        # 错误类型
        if error_info["error_type"]:
            error_type_map = {
                "syntax": "语法错误",
                "keyword": "关键字冲突",
                "duplicate": "重复定义",
                "reference": "未定义引用",
            }
            type_name = error_type_map.get(error_info["error_type"], "未知类型")
            lines.append(f"🔍 错误类型：{type_name}")

        # 错误信息
        if error_info["error_message"]:
            # 简化错误信息
            error_msg = error_info["error_message"]
            if len(error_msg) > 100:
                error_msg = error_msg[:97] + "..."
            lines.append(f"💡 错误信息：{error_msg}")

        # 修复建议
        if error_info["suggestion"]:
            lines.append("")
            lines.append(f"✨ 修复建议：{error_info['suggestion']}")

        return "\n".join(lines)

    # ========== 主题检测 ==========

    def _detect_theme(self, content: str) -> str:
        """
        智能检测当前主题

        Returns:
            'dark', 'light', 或 'unknown'
        """
        # 检查主题配置
        theme_match = re.search(r"'theme'\s*:\s*'([^']+)'", content)
        if theme_match:
            theme = theme_match.group(1).lower()
            if theme in ["dark", "dark-preset", "darkblue"]:
                return "dark"
            elif theme in ["default", "forest", "neutral", "base"]:
                return "light"

        # 检查 themeVariables 中的 background
        bg_match = re.search(r"'background'\s*:\s*['\"]#([0-9a-fA-F]{6})", content)
        if bg_match:
            bg_hex = bg_match.group(1)
            # 判断背景亮度
            bg_rgb = hex_to_rgb(bg_hex)
            bg_luminance = get_luminance(bg_rgb)
            if bg_luminance < 0.5:
                return "dark"
            else:
                return "light"

        # 默认为 light
        return "light"

    # ========== 颜色对比度检查增强 ==========

    def _check_classdef_contrast(self, content: str) -> Dict[str, Any]:
        """检查 classDef 定义的颜色对比度"""
        result = {"checked": False, "issues": [], "suggestions": []}

        # 查找所有 classDef 定义
        # 支持多行和单行格式
        classdef_pattern = r"classDef\s+(\w+)\s+([^;\n]+)"
        classdefs = re.findall(classdef_pattern, content)

        if not classdefs:
            return result

        result["checked"] = True

        # 检测主题
        theme = self._detect_theme(content)
        default_text_rgb = (248, 249, 250) if theme == "dark" else (51, 51, 51)

        low_contrast_classes = []

        for class_name, style_def in classdefs:
            # 提取 fill 和 color
            fill_match = re.search(r"fill:#([0-9a-fA-F]{6})", style_def)
            color_match = re.search(r"color:#([0-9a-fA-F]{6})", style_def)

            if fill_match:
                fill_rgb = hex_to_rgb(fill_match.group(1))

                # 如果指定了 color，使用指定的；否则使用默认
                text_rgb = default_text_rgb
                if color_match:
                    text_rgb = hex_to_rgb(color_match.group(1))

                # 计算对比度
                contrast = get_contrast_ratio(fill_rgb, text_rgb)

                if contrast < 4.5:
                    low_contrast_classes.append(
                        {
                            "class": class_name,
                            "fill": fill_match.group(1),
                            "color": color_match.group(1) if color_match else None,
                            "contrast": round(contrast, 2),
                        }
                    )

        if low_contrast_classes:
            result["issues"].append(
                f"发现{len(low_contrast_classes)}个 classDef 对比度不足（WCAG AA 要求 4.5:1）"
            )
            for item in low_contrast_classes:
                color_info = f", color:#{item['color']}" if item['color'] else ""
                result["suggestions"].append(
                    f"  • classDef {item['class']} (fill:#{item['fill']}{color_info}): "
                    f"对比度 {item['contrast']}:1"
                )
        else:
            result["suggestions"].append("✅ classDef 颜色对比度符合WCAG AA标准")

        return result

    def _check_theme_variables_contrast(self, content: str) -> Dict[str, Any]:
        """检查 themeVariables 的颜色对比度"""
        result = {"checked": False, "issues": [], "suggestions": []}

        # 查找 themeVariables
        tv_match = re.search(
            r"'themeVariables'\s*:\s*\{([^}]+)\}", content, re.DOTALL
        )
        if not tv_match:
            return result

        result["checked"] = True

        variables_str = tv_match.group(1)

        # 提取主要颜色变量
        color_vars = {}
        var_patterns = [
            (r"'primaryColor'\s*:\s*'#([0-9a-fA-F]{6})'", "primaryColor"),
            (r"'secondaryColor'\s*:\s*'#([0-9a-fA-F]{6})'", "secondaryColor"),
            (r"'tertiaryColor'\s*:\s*'#([0-9a-fA-F]{6})'", "tertiaryColor"),
            (r"'background'\s*:\s*'#([0-9a-fA-F]{6})'", "background"),
            (r"'primaryTextColor'\s*:\s*'#([0-9a-fA-F]{6})'", "primaryTextColor"),
            (r"'secondaryTextColor'\s*:\s*'#([0-9a-fA-F]{6})'", "secondaryTextColor"),
            (r"'lineColor'\s*:\s*'#([0-9a-fA-F]{6})'", "lineColor"),
        ]

        for pattern, var_name in var_patterns:
            match = re.search(pattern, variables_str)
            if match:
                color_vars[var_name] = match.group(1)

        # 检查主要对比度
        issues = []
        if "primaryColor" in color_vars and "primaryTextColor" in color_vars:
            fill_rgb = hex_to_rgb(color_vars["primaryColor"])
            text_rgb = hex_to_rgb(color_vars["primaryTextColor"])
            contrast = get_contrast_ratio(fill_rgb, text_rgb)

            if contrast < 4.5:
                issues.append(
                    f"  • primaryColor vs primaryTextColor: 对比度 {round(contrast, 2)}:1 "
                    f"(#{color_vars['primaryColor']} vs #{color_vars['primaryTextColor']})"
                )

        if "secondaryColor" in color_vars and "secondaryTextColor" in color_vars:
            fill_rgb = hex_to_rgb(color_vars["secondaryColor"])
            text_rgb = hex_to_rgb(color_vars["secondaryTextColor"])
            contrast = get_contrast_ratio(fill_rgb, text_rgb)

            if contrast < 4.5:
                issues.append(
                    f"  • secondaryColor vs secondaryTextColor: 对比度 {round(contrast, 2)}:1 "
                    f"(#{color_vars['secondaryColor']} vs #{color_vars['secondaryTextColor']})"
                )

        # 检查背景与lineColor的对比度
        if "background" in color_vars and "lineColor" in color_vars:
            bg_rgb = hex_to_rgb(color_vars["background"])
            line_rgb = hex_to_rgb(color_vars["lineColor"])
            contrast = get_contrast_ratio(bg_rgb, line_rgb)

            if contrast < 3.0:  # 稍低的标准
                issues.append(
                    f"  • background vs lineColor: 对比度 {round(contrast, 2)}:1 "
                    f"(#{color_vars['background']} vs #{color_vars['lineColor']})"
                )

        if issues:
            result["issues"].append(
                f"发现 {len(issues)} 处 themeVariables 对比度不足"
            )
            result["suggestions"].extend(issues)
            result["suggestions"].append(
                "💡 建议调整颜色使对比度至少达到 WCAG AA 标准（4.5:1）"
            )
        else:
            result["suggestions"].append("✅ themeVariables 颜色对比度符合标准")

        return result

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
                    # 使用新的错误解析功能
                    error_parts = []
                    if result.returncode != 0:
                        error_parts.append(f"退出码: {result.returncode}")
                    if result.stderr:
                        error_parts.append(result.stderr)
                    if result.stdout:
                        error_parts.append(result.stdout)

                    error_msg = " | ".join(error_parts) if error_parts else "未知错误"

                    # 尝试解析错误并生成友好的错误报告
                    if self.content_cache:
                        error_info = self._parse_mermaid_error(error_msg, self.content_cache)
                        if error_info["line_number"] or error_info["error_type"]:
                            # 成功解析错误，返回格式化的错误报告
                            return False, self._format_error_report(error_info)

                    # 无法解析，返回原始错误信息
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
        """检查颜色对比度（增强版：检查style、classDef、themeVariables）"""
        result = {
            "checked": False,
            "style": {"checked": False, "issues": [], "suggestions": []},
            "classdef": {"checked": False, "issues": [], "suggestions": []},
            "theme_variables": {"checked": False, "issues": [], "suggestions": []},
            "issues": [],
            "suggestions": [],
        }

        # 1. 检查 style 定义中的颜色对比度
        # 增强模式：检查 fill、stroke 和 color 属性
        style_patterns = re.findall(
            r"style\s+(\w+)\s+([^;]+)", content,
        )

        if style_patterns:
            result["checked"] = True
            result["style"]["checked"] = True

            # 检测主题
            theme = self._detect_theme(content)
            default_text_rgb = (248, 249, 250) if theme == "dark" else (51, 51, 51)

            low_contrast_nodes = []

            for node_id, style_def in style_patterns:
                # 提取 fill 和 color
                fill_match = re.search(r"fill:#([0-9a-fA-F]{6})", style_def)
                color_match = re.search(r"color:#([0-9a-fA-F]{6})", style_def)

                if fill_match:
                    fill_rgb = hex_to_rgb(fill_match.group(1))

                    # 如果指定了 color，使用指定的；否则使用默认
                    text_rgb = default_text_rgb
                    if color_match:
                        text_rgb = hex_to_rgb(color_match.group(1))

                    # 计算对比度
                    contrast = get_contrast_ratio(fill_rgb, text_rgb)

                    # WCAG AA 标准：至少 4.5:1
                    if contrast < 4.5:
                        color_info = f", color:#{color_match.group(1)}" if color_match else ""
                        low_contrast_nodes.append(
                            {
                                "node": node_id,
                                "fill": fill_match.group(1),
                                "color": color_match.group(1) if color_match else None,
                                "contrast": round(contrast, 2),
                            }
                        )

            if low_contrast_nodes:
                result["style"]["issues"].append(
                    f"发现{len(low_contrast_nodes)}个节点对比度不足（WCAG AA 要求 4.5:1）"
                )
                for item in low_contrast_nodes:
                    color_info = f", color:#{item['color']}" if item['color'] else ""
                    result["style"]["suggestions"].append(
                        f"  • 节点 {item['node']} (fill:#{item['fill']}{color_info}): "
                        f"对比度 {item['contrast']}:1"
                    )
                result["style"]["suggestions"].append(
                    "💡 修复建议：\n"
                    "   1. 浅色背景用深色文字（#333）\n"
                    "   2. 深色背景用浅色文字（#f8f9fa）\n"
                    "   3. 使用预定义主题避免手动调色"
                )
            else:
                result["style"]["suggestions"].append("✅ style 颜色对比度符合WCAG AA标准")

        # 2. 检查 classDef 定义中的颜色对比度
        classdef_result = self._check_classdef_contrast(content)
        result["classdef"] = classdef_result
        if classdef_result["checked"]:
            result["checked"] = True

        # 3. 检查 themeVariables 中的颜色对比度
        themevar_result = self._check_theme_variables_contrast(content)
        result["theme_variables"] = themevar_result
        if themevar_result["checked"]:
            result["checked"] = True

        # 汇总所有问题和建议
        all_issues = []
        all_suggestions = []

        for check_name in ["style", "classdef", "theme_variables"]:
            check_result = result[check_name]
            if check_result.get("issues"):
                all_issues.extend(check_result["issues"])
            if check_result.get("suggestions"):
                all_suggestions.extend(check_result["suggestions"])

        result["issues"] = all_issues
        result["suggestions"] = all_suggestions

        # 如果没有任何检查，返回未检查状态
        if not result["checked"]:
            result["suggestions"].append("未找到颜色定义，无需检查对比度")

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

    # ========== 自动修复功能 ==========

    def auto_fix_issues(
        self,
        content: str,
        fix_types: list = None,
        dry_run: bool = False
    ) -> Tuple[str, Dict[str, Any]]:
        """
        自动修复常见问题

        Args:
            content: 文件内容
            fix_types: 要修复的类型列表 ['theme', 'contrast', 'syntax', 'labels']
            dry_run: 是否为预览模式（不实际修改）

        Returns:
            (修复后的内容, 修复报告)
        """
        if fix_types is None:
            fix_types = ["theme", "contrast", "syntax", "labels"]

        result = {
            "fixed": [],
            "skipped": [],
            "errors": [],
            "dry_run": dry_run
        }

        fixed_content = content

        # 1. 修复主题缺失
        if "theme" in fix_types:
            fixed_content, theme_fixes = self._fix_missing_theme(fixed_content)
            result["fixed"].extend(theme_fixes)

        # 2. 修复废弃语法
        if "syntax" in fix_types:
            fixed_content, syntax_fixes = self._fix_deprecated_syntax(fixed_content)
            result["fixed"].extend(syntax_fixes)

        # 3. 修复标签过长
        if "labels" in fix_types:
            fixed_content, label_fixes = self._fix_long_labels(fixed_content)
            result["fixed"].extend(label_fixes)

        # 4. 修复颜色对比度
        if "contrast" in fix_types:
            fixed_content, contrast_fixes = self._fix_contrast_issues(fixed_content)
            result["fixed"].extend(contrast_fixes)

        return fixed_content, result

    def _fix_missing_theme(self, content: str) -> Tuple[str, list]:
        """修复缺失的主题配置"""
        fixes = []

        # 检查是否已有主题配置
        has_init = "%%{init:" in content
        has_config = "---" in content and "config:" in content

        if has_init or has_config:
            return content, fixes

        # 检测主题类型
        has_dark_keywords = any(
            kw in content.lower() for kw in ["dark", "night", "black"]
        )

        theme = "dark" if has_dark_keywords else "default"

        # 在文件开头插入主题配置
        lines = content.split("\n")
        mermaid_start = -1

        # 找到 ```mermaid 所在行
        for i, line in enumerate(lines):
            if "mermaid" in line.lower():
                mermaid_start = i
                break

        if mermaid_start >= 0:
            # 在 ```mermaid 后插入主题配置
            lines.insert(mermaid_start + 1, f"%%{{init: {{'theme':'{theme}'}}}}%%")
            fixes.append(f"添加主题配置：{theme}")
        else:
            # 直接在开头插入
            lines.insert(0, f"%%{{init: {{'theme':'{theme}'}}}}%%")
            fixes.append(f"添加主题配置：{theme}")

        return "\n".join(lines), fixes

    def _fix_deprecated_syntax(self, content: str) -> Tuple[str, list]:
        """修复废弃的 graph 语法"""
        fixes = []
        fixed_content = content

        # 检查是否使用了 graph 而不是 flowchart
        graph_pattern = r"\bgraph\s+(TD|TB|LR|RL|BT)"

        matches = list(re.finditer(graph_pattern, fixed_content, re.IGNORECASE))

        if matches:
            # 替换为 flowchart
            fixed_content = re.sub(
                r"\bgraph\s+(TD|TB|LR|RL|BT)",
                r"flowchart \1",
                fixed_content,
                count=1  # 只替换第一个
            )
            fixes.append(f"将 'graph' 替换为 'flowchart'")

        return fixed_content, fixes

    def _fix_long_labels(self, content: str) -> Tuple[str, list]:
        """修复过长的标签"""
        fixes = []
        fixed_content = content
        max_length = 25

        # 查找所有标签
        label_pattern = r"\[([^\]]+)\]"

        def shorten_label(match):
            label = match.group(1)

            # 跳过已经是简短的标签或包含引号的标签
            if len(label) <= max_length or label.startswith('"'):
                return match.group(0)

            # 简化标签（取前 max_length 个字符并添加省略号）
            shortened = label[:max_length-3] + "..."
            fixes.append(f"缩短标签：'{label}' → '{shortened}'")

            return f'["{shortened}"]'

        fixed_content = re.sub(label_pattern, shorten_label, fixed_content)

        return fixed_content, fixes

    def _fix_contrast_issues(self, content: str) -> Tuple[str, list]:
        """修复颜色对比度问题（简化版）"""
        fixes = []
        fixed_content = content

        # 检测主题
        theme = self._detect_theme(content)

        # 为浅色背景的节点添加文字颜色
        if theme == "light":
            # 浅色背景应该用深色文字
            # 查找浅色填充但没有指定文字颜色的样式
            pattern = r"(style\s+\w+\s+[^;]*?fill:#(?:[e-f][0-9a-f]|[f][0-9a]){6}[^\n]*?)(?:,|\s*$)"

            def add_color_to_light_style(match):
                style_def = match.group(1)

                # 检查是否已有 color 属性
                if "color:" in style_def:
                    return match.group(0)

                # 添加深色文字
                fixed_style = style_def.rstrip(", ")
                if not fixed_style.endswith(","):
                    fixed_style += ", "
                fixed_style += "color:#333"

                fixes.append("为浅色背景节点添加深色文字 (#333)")

                return fixed_style

            fixed_content = re.sub(pattern, add_color_to_light_style, fixed_content)

        return fixed_content, fixes

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
    parser.add_argument(
        "--fix",
        nargs="?",
        const="all",
        choices=["all", "theme", "contrast", "syntax", "labels"],
        help="自动修复常见问题（可选：all, theme, contrast, syntax, labels）",
    )
    parser.add_argument(
        "--fix-dry-run",
        action="store_true",
        help="预览修复（不实际修改文件）",
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

    # 自动修复模式
    if args.fix:
        # 读取文件内容
        try:
            with open(args.filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"❌ 读取文件失败: {e}")
            sys.exit(1)

        # 确定要修复的类型
        fix_types = None  # None 表示修复所有类型
        if args.fix != "all":
            fix_types = [args.fix]

        # 执行修复
        print(f"{'🔍 预览修复' if args.fix_dry_run else '🔧 自动修复'}...")
        print()

        fixed_content, fix_result = validator.auto_fix_issues(
            content,
            fix_types=fix_types,
            dry_run=args.fix_dry_run
        )

        # 显示修复结果
        if fix_result["fixed"]:
            print("✅ 已修复以下问题：")
            for fix in fix_result["fixed"]:
                print(f"   • {fix}")
        else:
            print("ℹ️  没有需要修复的问题")

        if fix_result["errors"]:
            print("\n⚠️  修复时遇到错误：")
            for error in fix_result["errors"]:
                print(f"   • {error}")

        # 如果不是预览模式且有修复，保存文件
        if not args.fix_dry_run and fix_result["fixed"]:
            # 创建备份
            backup_path = args.filepath + ".backup"
            try:
                shutil.copy2(args.filepath, backup_path)
                print(f"\n💾 备份已保存到: {backup_path}")
            except Exception as e:
                print(f"\n⚠️  创建备份失败: {e}")

            # 保存修复后的内容
            try:
                with open(args.filepath, "w", encoding="utf-8") as f:
                    f.write(fixed_content)
                print(f"✅ 修复后的内容已保存到: {args.filepath}")
            except Exception as e:
                print(f"❌ 保存文件失败: {e}")
                sys.exit(1)

        print()

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
