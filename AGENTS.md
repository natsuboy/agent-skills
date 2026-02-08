# Agent Skills 代码规范指南

本文档为 agentic coding agents 提供在 agent-skills 仓库中工作的指导规范。

## 1. 构建/验证/发布命令

### 1.1 核心管理命令

```bash
make help                                # 查看所有可用命令
make init                                # 初始化仓库
make create SKILL_NAME=mermaid           # 创建新 Skill
make tag SKILL_NAME=mermaid VERSION=1.0.0 # 打标并发布 Skill
```

### 1.2 Skill 验证和预览命令

```bash
# 验证单个 skill
make validate SKILL_NAME=mermaid

# 验证所有 skills
make validate-all

# 预览单个 skill
make preview SKILL_NAME=mermaid

# 列出所有 skills
make preview-all
```

### 1.3 Skill 发布命令

```bash
# 完整发布流程（验证 + 打标 + 推送）
make publish SKILL_NAME=mermaid VERSION=1.0.0

# 为单个 skill 打标
make tag SKILL_NAME=mermaid VERSION=1.0.0

# 批量为所有 skills 打标
make tag-all
```

**发布流程说明**：
1. `tag_skill.sh` 验证 skill 符合规范
2. 创建 Git tag（格式：`<skill-name>-v<version>`）
3. 推送 tag 到远程仓库
4. **GitHub Actions 自动创建 Release**
5. 用户可通过 `npx skills` 安装

### 1.4 代码检查命令

```bash
# 运行所有检查
make lint

# 自动修复问题
make lint-fix
```

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

**章节编号**：必须从 1 开始连续递归，## 为主章节，### 为子章节

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
- 章节编号：从 1 开始连续递归
**注释规范**：
- Bash：单行 `# 注释` 或块注释说明功能
- Python：使用 docstring，包含 Args 和 Returns

---

## 4. Git 使用规范

**提交格式**：`类型(范围): 简短描述`
- 类型：feat/fix/docs/chore/refactor
- 示例：`feat(mermaid): 添加颜色对比度检查`

**分支规范**：`main`（稳定）、`develop`（开发）、`feature/skill-name`（功能）、`fix/issue-name`（修复）

**Tag 格式**：`<skill-name>-v<version>`（例如：`mermaid-v1.0.0`）

---

## 5. 开发工作流

### 5.1 新 Skill 开发流程

```bash
# 1. 创建 skill 框架
make create SKILL_NAME=my-new-skill

# 2. 编辑 SKILL.md（必须包含 YAML frontmatter）
# 示例：
# ---
# name: my-new-skill
# description: 我的技能描述
# ---

# 3. 实现功能和文档

# 4. 验证 skill
make validate SKILL_NAME=my-new-skill

# 5. 预览效果
make preview SKILL_NAME=my-new-skill

# 6. 提交代码
make commit MESSAGE="feat(my-new-skill): 添加新技能"
make push

# 7. 打标并发布
make publish SKILL_NAME=my-new-skill VERSION=1.0.0
```

### 5.2 现有 Skill 修改流程

```bash
# 1. 修改代码/文档

# 2. 验证修改
make validate SKILL_NAME=mermaid

# 3. 预览效果
make preview SKILL_NAME=mermaid

# 4. 提交代码
make commit MESSAGE="fix(mermaid): 修复语法错误"
make push

# 5. 打新版本
make tag SKILL_NAME=mermaid VERSION=1.1.0
```

---

## 6. 验证清单

提交前确保：
- ✓ 所有脚本有 Shebang 和头部注释
- ✓ Bash 脚本使用 `set -e` 和 `set -u`
- ✓ Python 代码通过 `ruff check`
- ✓ 文档使用简体中文
- ✓ 关键代码有中文注释
- ✓ JSON 格式正确
- ✓ 文件命名遵循约定
- ✓ **SKILL.md 包含正确的 YAML frontmatter**
- ✓ **通过 `./scripts/validate_skill.sh` 验证**

---

## 7. 常见问题

**Q: 如何使用 Make？**
运行 `make help` 查看所有可用命令。示例：
- `make validate SKILL_NAME=mermaid`
- `make tag SKILL_NAME=mermaid VERSION=1.0.0`
- `make publish SKILL_NAME=mermaid VERSION=1.0.0`

**Q: 如何测试脚本？**
使用 `make <command>`

**Q: Python 环境要求？**
Python 3.8+，部分功能需 Node.js

**Q: 如何调试 Bash？**
使用 `bash -x script-name.sh`

**Q: 需要运行 lint 吗？**
运行 `make lint` 或 `ruff check --fix .` 检查 Python 代码

**Q: 项目有测试吗？**
当前无自动化测试，手动运行脚本验证功能

**Q: 如何发布 skill？**
运行 `make tag SKILL_NAME=mermaid VERSION=1.0.0`，GitHub Actions 会自动创建 Release

**Q: tag 格式是什么？**
`<skill-name>-v<version>`，例如：`mermaid-v1.0.0`

**Q: 如何验证 skill？**
运行 `make validate SKILL_NAME=mermaid`

**Q: 如何预览 skill？**
运行 `make preview SKILL_NAME=mermaid`

---

## 8. 工具函数说明

### 8.1 utils.sh 提供的函数

**日志函数**：
- `log_step [step_num] "message"` - 输出步骤信息
- `log_success "message"` - 输出成功信息
- `log_error "message"` - 输出错误信息并退出
- `log_warning "message"` - 输出警告信息

**工具函数**：
- `validate_version "version"` - 验证语义化版本号
- `extract_yaml_field "skill_dir" "field"` - 提取 SKILL.md 中的字段
- `get_skill_config "skill_name" "field"` - 获取 skills.json 配置
- `get_all_skills` - 获取所有 skill 名称列表
- `skill_exists "skill_name"` - 检查 skill 是否存在
- `validate_yaml_frontmatter "skill_file"` - 验证 YAML frontmatter 格式
- `generate_release_notes "skill_name" "version"` - 生成 Release Notes

**跨平台函数**：
- `portable_sed_inplace "pattern" "file"` - 跨平台 sed 替换
- `escape_sed_pattern "text"` - 转义 sed 特殊字符
- `get_sha256_cmd` - 获取 SHA256 命令
- `check_command "command"` - 检查命令是否存在

---

## 9. GitHub Actions 工作流

### 9.1 自动发布工作流

**触发条件**：推送 tag 格式为 `*-v*`（例如：`mermaid-v1.0.0`）

**执行流程**：
1. 解析 tag 名称，提取 skill name 和 version
2. 验证 skill 目录存在
3. 运行 `validate_skill.sh` 验证
4. 生成 Release Notes
5. 创建 GitHub Release

**查看 Release**：访问 `https://github.com/natsuboy/agent-skills/releases`

---

## 10. skills.sh 生态集成

本项目完全兼容 [skills.sh](https://skills.sh) 生态系统。

### 10.1 目录结构要求

skills.sh 会扫描以下位置：
- `skills/`（推荐）
- `skills/.curated/`
- `skills/.experimental/`
- `skills/.system/`
- 根目录（如果包含 SKILL.md）

### 10.2 SKILL.md 格式要求

```yaml
---
name: skill-name
description: 简短描述
metadata:
  internal: true  # 可选，设为 true 隐藏该 skill
---
# Skill 文档内容
```

**必需字段**：
- `name`：唯一标识符（小写，允许连字符）
- `description`：简要说明

### 10.3 用户安装

```bash
# 安装所有 skills
npx skills add natsuboy/agent-skills

# 安装特定 skill
npx skills add natsuboy/agent-skills --skill mermaid

# 列出可用 skills
npx skills add natsuboy/agent-skills --list
```
