# Agent Skills 代码规范指南

本文档为 agentic coding agents 提供在 agent-skills 仓库中工作的指导规范。

## 1. 构建/Lint/测试命令

### 1.1 核心管理命令

```bash
./scripts/init.sh                       # 初始化仓库
./scripts/create_skill.sh <skill-name> # 创建新 Skill
./scripts/publish.sh <skill-name> <version> # 发布 Skill
```

### 1.2 代码检查命令

```bash
# Python Lint（使用 Ruff）
ruff check .                    # 检查所有 Python 文件
ruff check --fix .              # 自动修复问题
# Bash 脚本检查
shellcheck scripts/*.sh         # 需先安装 shellcheck
```

### 1.3 验证命令

```bash
# Mermaid 验证（仅 mermaid skill）
python3 skills/mermaid/scripts/validate_mermaid.py diagram.md
python3 skills/mermaid/scripts/validate_mermaid.py diagram.md --verbose
```

**注意**：当前项目没有自动化测试框架。测试通过手动运行脚本验证功能。

---

## 2. 代码风格指南

### 2.1 Bash 脚本规范

**头部格式（强制）**：
```bash
#!/bin/bash
##############################################################################
# [项目名称] - [脚本功能简述]
# 用法: ./scripts/script-name.sh <args>
##############################################################################
set -e  # 遇到错误立即退出
set -u  # 使用未定义变量时报错
```

**日志函数（统一使用 utils.sh）**：
```bash
source "$(dirname "$0")/utils.sh"
log_step "正在执行操作"
log_success "操作成功"
log_error "操作失败"
log_warning "警告信息"
```

**跨平台兼容**：使用 `portable_sed_inplace` 替代 `sed -i`（已在 utils.sh 中定义），使用 `$(dirname "$0")` 获取脚本目录，检查命令存在性：`check_command jq`

**变量命名**：全局变量用 `UPPER_SNAKE_CASE`，局部变量用 `lower_snake_case`

---

### 2.2 Python 脚本规范

**基础格式**：
```python
#!/usr/bin/env python3
"""模块/脚本文档字符串（功能说明、使用方法、返回码）"""
from pathlib import Path
from typing import List, Dict, Tuple, Any
```

**类型提示（强制）**：使用 `-> Tuple[bool, str]` 等类型注解，docstring 包含 Args 和 Returns

**导入顺序**：标准库 → 第三方库 → 本地模块

**命名规则**：类用 PascalCase（如 `MermaidValidator`），函数/变量用 snake_case（如 `check_and_install_cli`），常量用 UPPER_SNAKE_CASE

**错误处理**：使用 try/except 捕获 subprocess 异常，sys.exit(1) 退出

---

### 2.3 Markdown 文档规范

**章节编号**：必须从 1 开始连续递增，## 为主章节，### 为子章节

**格式要求**：中文段落，代码块指定语言，表格对齐，添加目录，关键代码加中文注释

---

### 2.4 命名约定

**文件名**：小写 + 连字符（kebab-case）如 `my-new-skill`

**目录结构**：
```
skills/<skill-name>/
├── SKILL.md           # 核心 skill 文档（必选）
├── README.md          # 用户文档（必选）
├── scripts/           # 脚本文件
├── references/        # 参考文档
└── assets/            # 资源文件（模板等）
```

**配置结构（skills.json）**：包含 name, displayName, version, description, author 等字段

---

## 3. 语言和文档要求

**强制要求**：
- 对话和文档语言：简体中文（代码和专业术语除外）
- 关键代码：必须加详细中文注释
- 文档格式：美观，使用表格/列表/代码块
- 章节编号：从 1 开始连续递增
**注释规范**：
- Bash：单行 `# 注释` 或块注释说明功能
- Python：使用 docstring，包含 Args 和 Returns

---

## 4. Git 使用规范

**提交格式**：`类型(范围): 简短描述`
- 类型：feat/fix/docs/chore/refactor
- 示例：`feat(mermaid): 添加颜色对比度检查`

**分支规范**：`main`（稳定）、`develop`（开发）、`feature/skill-name`（功能）、`fix/issue-name`（修复）

---

## 5. 验证清单

提交前确保：
- ✓ 所有脚本有 Shebang 和头部注释
- ✓ Bash 脚本使用 `set -e` 和 `set -u`
- ✓ Python 代码通过 `ruff check`
- ✓ 文档使用简体中文
- ✓ 关键代码有中文注释
- ✓ JSON 格式正确
- ✓ 文件命名遵循约定

---

## 6. 常见问题

**Q: 如何测试脚本？** 直接运行 `./scripts/script-name.sh`

**Q: Python 环境要求？** Python 3.8+，部分功能需 Node.js

**Q: 如何调试 Bash？** 使用 `bash -x script-name.sh`

**Q: 需要运行 lint 吗？** 运行 `ruff check --fix .` 检查 Python 代码

**Q: 项目有测试吗？** 当前无自动化测试，手动运行脚本验证功能
