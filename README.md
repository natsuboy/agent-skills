# Agent Skills

我的 Agent Skills 集合，采用模块化结构组织，便于开发和发布。本项目为 AI Agent 提供可复用的技能包，每个 Skill 都是独立可安装的功能模块。

## 1. 项目简介

Agent Skills 是一个专为 AI Agent 设计的技能库，提供高质量的、可复用的 Skill 模块。每个 Skill 都包含完整的文档、脚本、参考和资源文件，可以直接集成到 AI Agent 的工具链中。

### 1.1 主要特性

- **模块化设计**：每个 Skill 独立开发、测试和发布
- **自动化工具**：提供完整的脚手架、验证和发布脚本
- **代码规范**：统一的代码风格和文档标准
- **高质量输出**：通过自动化验证确保 Skill 质量
- **skills.sh 兼容**：完全兼容 [skills.sh](https://skills.sh) 生态系统

## 2. 项目结构

```
agent-skills/
├── skills/                 # 所有 Skill 实现
│   └── mermaid/           # Mermaid 图表生成 Skill
│       ├── SKILL.md       # 核心 Skill 文档
│       ├── README.md      # 用户文档
│       ├── scripts/       # 脚本文件
│       ├── references/    # 参考文档
│       └── assets/        # 资源文件
├── scripts/               # 通用管理工具
│   ├── init.sh           # 初始化仓库
│   ├── create_skill.sh   # 创建新 Skill
│   ├── validate_skill.sh # 验证 Skill
│   ├── preview_skill.sh  # 预览 Skill
│   ├── tag_skill.sh      # 为 Skill 打标
│   └── utils.sh          # 工具函数库
├── .github/workflows/     # GitHub Actions
│   └── release.yml       # 自动发布工作流
├── AGENTS.md             # Agent 开发规范
├── README.md             # 项目文档
└── skills.json           # Skills 配置注册表
```

### 2.1 核心目录说明

- **`skills/`**：包含所有 Skill 实现，每个子目录都是独立的 Skill
- **`scripts/`**：提供仓库管理和 Skill 开发的自动化脚本
- **`skills.json`**：所有 Skills 的中央配置注册表
- **`.github/workflows/`**：自动化发布工作流

## 3. 快速开始

### 3.1 安装 Skills

#### 使用 skills.sh CLI（推荐）

```bash
# 安装所有 skills
npx skills add natsuboy/agent-skills

# 安装特定 skill
npx skills add natsuboy/agent-skills --skill mermaid

# 列出可用 skills
npx skills add natsuboy/agent-skills --list
```

#### 手动安装

```bash
# 克隆仓库
git clone https://github.com/natsuboy/agent-skills.git

# 复制 skill 到你的 agent 的 skills 目录
# Claude Code
cp -r agent-skills/skills/mermaid ~/.claude/skills/

# 或复制到项目目录
cp -r agent-skills/skills/mermaid .claude/skills/
```

### 3.2 初始化仓库

如果你刚克隆了这个仓库，运行此命令来设置你的作者信息：

```bash
./scripts/init.sh
```

此脚本将：
- 替换配置文件中的占位符（用户名、作者信息）
- 设置 Git 配置
- 验证开发环境

### 3.3 创建新 Skill

无需手动复制文件，使用脚手架快速开始：

```bash
# 用法: ./scripts/create_skill.sh <skill-name>
./scripts/create_skill.sh my-new-skill
```

创建脚本会自动：
- 创建 `skills/my-new-skill` 目录结构
- 生成基础文档（SKILL.md, README.md）
- 在 `skills.json` 中注册新 Skill
- 创建示例脚本和资源文件

## 4. 开发流程

### 4.1 本地开发

开发新 Skill 或修改现有 Skill 时，遵循以下流程：

```bash
# 1. 创建/修改 skill
make create SKILL_NAME=my-new-skill

# 2. 验证 skill
make validate SKILL_NAME=mermaid

# 3. 预览 skill（查看安装效果）
make preview SKILL_NAME=mermaid

# 4. 开发验证（验证 + 预览）
make dev
```

### 4.2 发布 Skill

当准备好发布时：

```bash
# 完整发布流程（验证 + 打标 + 推送）
make publish SKILL_NAME=mermaid VERSION=1.0.0

# 或分步执行
make tag SKILL_NAME=mermaid VERSION=1.0.0
make push-tags
```

**发布流程**：
1. 验证 Skill 符合规范
2. 创建 Git tag（格式：`my-new-skill-v1.0.0`）
3. 推送 tag 到远程仓库
4. **GitHub Actions 自动创建 Release**
5. 用户可通过 `npx skills` 安装

### 4.3 可用管理命令

| 命令 | 功能 | 示例 |
|------|------|------|
| `make validate` | 验证 Skill 规范 | `make validate SKILL_NAME=mermaid` |
| `make preview` | 预览 Skill 信息 | `make preview SKILL_NAME=mermaid` |
| `make tag` | 为 Skill 打标 | `make tag SKILL_NAME=mermaid VERSION=1.0.0` |
| `make publish` | 完整发布流程 | `make publish SKILL_NAME=mermaid VERSION=1.0.0` |
| `make create` | 创建新 Skill | `make create SKILL_NAME=my-skill` |
| `make dev` | 开发验证 | `make dev` |
| `make lint` | 代码检查 | `make lint` |

**查看所有命令**：运行 `make help`

## 5. 可用 Skills

| Skill | 描述 | 安装 |
|-------|------|------|
| **[Mermaid](skills/mermaid/README.md)** | 专业的 Mermaid 图表生成 Skill，提供高质量、美观、语法正确的图表创建能力 | `npx skills add natsuboy/agent-skills --skill mermaid` |

查看 [SKILLS.md](SKILLS.md) 获取完整技能清单。

## 6. 开发指南

### 6.1 代码规范

本项目遵循严格的代码规范，详见 [AGENTS.md](AGENTS.md) 文档。

#### 6.1.1 代码检查

```bash
# Python Lint（使用 Ruff）
ruff check .                    # 检查所有 Python 文件
ruff check --fix .              # 自动修复问题

# Bash 脚本检查（需先安装 shellcheck）
shellcheck scripts/*.sh
```

#### 6.1.2 验证命令

```bash
make validate SKILL_NAME=mermaid      # 验证单个 skill
make validate-all                     # 验证所有 skills
make preview SKILL_NAME=mermaid      # 预览 skill
```

**注意**：当前项目没有自动化测试框架。测试通过手动运行脚本验证功能。

### 6.2 Skill 开发流程

1. 使用 `create_skill.sh` 创建 Skill 框架
2. 在 `SKILL.md` 中定义 Agent 指令集（包含 YAML frontmatter）
3. 实现必要的脚本和工具
4. 添加参考文档和资源
5. 更新 `skills.json` 配置
6. 本地验证：`./scripts/validate_skill.sh <skill-name>`
7. 预览效果：`./scripts/preview_skill.sh <skill-name>`
8. 打标发布：`./scripts/tag_skill.sh <skill-name> <version>`

### 6.3 命名约定

- **Skill 名称**：小写 + 连字符（kebab-case），如 `my-new-skill`
- **目录结构**：
  ```
  skills/<skill-name>/
  ├── SKILL.md           # 核心 skill 文档（必选）
  ├── README.md          # 用户文档（必选）
  ├── scripts/           # 脚本文件
  ├── references/        # 参考文档
  └── assets/            # 资源文件（模板等）
  ```
- **Git tag 格式**：`<skill-name>-v<version>`（例如：`mermaid-v1.0.0`）

## 7. Git 使用规范

### 7.1 提交格式

```
类型(范围): 简短描述
```

**类型**：
- `feat`: 新功能
- `fix`: 修复
- `docs`: 文档更新
- `chore`: 构建或辅助工具变动
- `refactor`: 重构

**示例**：
- `feat(mermaid): 添加颜色对比度检查`
- `fix(release): 修复 tag 解析错误`
- `docs(readme): 更新安装说明`

### 7.2 分支规范

- `main`：稳定版本
- `develop`：开发版本
- `feature/skill-name`：功能分支
- `fix/issue-name`：修复分支

## 8. 验证清单

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

## 9. 常见问题

### Q: 如何安装 skills？

**推荐方式**：使用 skills.sh CLI
```bash
npx skills add natsuboy/agent-skills
```

**手动方式**：克隆仓库并复制到 agent 的 skills 目录

### Q: 如何使用 Make？

运行 `make help` 查看所有可用命令。常用命令：
```bash
make validate              # 验证所有 skills
make validate mermaid      # 验证单个 skill
make tag mermaid 1.0.0   # 为 skill 打标
make publish              # 完整发布流程
```

### Q: 如何测试脚本？

使用 `make <command>`

### Q: Python 环境要求？

Python 3.8+，部分功能需 Node.js

### Q: 如何调试 Bash？

使用 `bash -x script-name.sh`

### Q: 需要运行 lint 吗？

运行 `make lint` 或 `ruff check --fix .` 检查 Python 代码

### Q: 项目有测试吗？

当前无自动化测试，手动运行脚本验证功能

### Q: 发布流程是怎样的？

```bash
make publish SKILL_NAME=mermaid VERSION=1.0.0

# GitHub Actions 自动创建 Release
# 访问 https://github.com/natsuboy/agent-skills/releases
```

### Q: skills.sh 是什么？

[skills.sh](https://skills.sh) 是由 Vercel 开发的开放 Agent Skills CLI 工具，用于统一管理和安装 AI Agent 的技能包。我们的项目完全兼容 skills.sh 生态系统。

## 10. 贡献指南

欢迎贡献新的 Skills 或改进现有 Skills！请遵循以下步骤：

1. Fork 本仓库
2. 创建功能分支（`git checkout -b feature/amazing-skill`）
3. 提交更改（`git commit -m 'feat(skill): 添加 Amazing Skill'`）
4. 推送到分支（`git push origin feature/amazing-skill`）
5. 创建 Pull Request

请确保所有代码符合本项目的规范要求。

## 11. 许可证

本项目采用 MIT 许可证。详见 LICENSE 文件。

---

**详细开发规范**：请参考 [AGENTS.md](AGENTS.md)

**技能清单**：请参考 [SKILLS.md](SKILLS.md)

**问题反馈**：[GitHub Issues](https://github.com/natsuboy/agent-skills/issues)
