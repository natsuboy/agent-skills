# Agent Skills

我的 Agent Skills 集合，采用模块化结构组织，便于开发和发布。本项目为 AI Agent 提供可复用的技能包，每个 Skill 都是独立可安装的功能模块。

## 1. 项目简介

Agent Skills 是一个专为 AI Agent 设计的技能库，提供高质量的、可复用的 Skill 模块。每个 Skill 都包含完整的文档、脚本、参考和资源文件，可以直接集成到 AI Agent 的工具链中。

### 1.1 主要特性

- **模块化设计**：每个 Skill 独立开发、测试和发布
- **自动化工具**：提供完整的脚手架、构建和发布脚本
- **代码规范**：统一的代码风格和文档标准
- **高质量输出**：通过自动化验证确保 Skill 质量

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
│   ├── publish.sh        # 发布 Skill
│   └── utils.sh          # 工具函数库
├── AGENTS.md             # Agent 开发规范
├── README.md             # 项目文档
└── skills.json           # Skills 配置注册表
```

### 2.1 核心目录说明

- **`skills/`**：包含所有 Skill 实现，每个子目录都是独立的 Skill
- **`scripts/`**：提供仓库管理和 Skill 开发的自动化脚本
- **`skills.json`**：所有 Skills 的中央配置注册表

## 3. 快速开始

### 3.1 初始化仓库

如果你刚克隆了这个仓库，运行此命令来设置你的作者信息：

```bash
./scripts/init.sh
```

此脚本将：
- 替换配置文件中的占位符（用户名、作者信息）
- 设置 Git 配置
- 验证开发环境

### 3.2 创建新 Skill

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

### 3.3 发布 Skill

当你准备好发布时：

```bash
# 用法: ./scripts/publish.sh <skill-name> <version>
./scripts/publish.sh mermaid 1.0.0
```

**发布流程**：
1. **构建**：在 `build/mermaid/` 生成 `.tar.gz` 包和 npm 安装器
2. **Git 发布**：提交代码并打标签（如 `mermaid-v1.0.0`）
3. **NPM 发布**：进入 `build/mermaid/installer` 运行 `npm publish`

## 4. 可用 Skills

| Skill | 描述 | 状态 |
|-------|------|------|
| **[Mermaid](skills/mermaid/README.md)** | 专业的 Mermaid 图表生成 Skill，提供高质量、美观、语法正确的图表创建能力 | ✅ Active |

## 5. 开发指南

### 5.1 代码规范

本项目遵循严格的代码规范，详见 [AGENTS.md](AGENTS.md) 文档。

#### 5.1.1 代码检查

```bash
# Python Lint（使用 Ruff）
ruff check .                    # 检查所有 Python 文件
ruff check --fix .              # 自动修复问题

# Bash 脚本检查（需先安装 shellcheck）
shellcheck scripts/*.sh
```

#### 5.1.2 验证命令

```bash
# Mermaid 验证（仅 mermaid skill）
python3 skills/mermaid/scripts/validate_mermaid.py diagram.md
python3 skills/mermaid/scripts/validate_mermaid.py diagram.md --verbose
```

**注意**：当前项目没有自动化测试框架。测试通过手动运行脚本验证功能。

### 5.2 Skill 开发流程

1. 使用 `create_skill.sh` 创建 Skill 框架
2. 在 `SKILL.md` 中定义 Agent 指令集
3. 实现必要的脚本和工具
4. 添加参考文档和资源
5. 更新 `skills.json` 配置
6. 本地验证功能
7. 使用 `publish.sh` 发布

### 5.3 命名约定

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

## 6. Git 使用规范

### 6.1 提交格式

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
- `fix(publish): 修复 npm 包构建错误`

### 6.2 分支规范

- `main`：稳定版本
- `develop`：开发版本
- `feature/skill-name`：功能分支
- `fix/issue-name`：修复分支

## 7. 验证清单

提交前确保：
- ✓ 所有脚本有 Shebang 和头部注释
- ✓ Bash 脚本使用 `set -e` 和 `set -u`
- ✓ Python 代码通过 `ruff check`
- ✓ 文档使用简体中文
- ✓ 关键代码有中文注释
- ✓ JSON 格式正确
- ✓ 文件命名遵循约定

## 8. 常见问题

### Q: 如何测试脚本？

直接运行 `./scripts/script-name.sh`

### Q: Python 环境要求？

Python 3.8+，部分功能需 Node.js

### Q: 如何调试 Bash？

使用 `bash -x script-name.sh`

### Q: 需要运行 lint 吗？

运行 `ruff check --fix .` 检查 Python 代码

### Q: 项目有测试吗？

当前无自动化测试，手动运行脚本验证功能

## 9. 贡献指南

欢迎贡献新的 Skills 或改进现有 Skills！请遵循以下步骤：

1. Fork 本仓库
2. 创建功能分支（`git checkout -b feature/amazing-skill`）
3. 提交更改（`git commit -m 'feat(skill): 添加 Amazing Skill'`）
4. 推送到分支（`git push origin feature/amazing-skill`）
5. 创建 Pull Request

请确保所有代码符合本项目的规范要求。

## 10. 许可证

本项目采用 MIT 许可证。详见 LICENSE 文件。

---

**详细开发规范**：请参考 [AGENTS.md](AGENTS.md)

**问题反馈**：[GitHub Issues](https://github.com/YOUR_USERNAME/agent-skills/issues)
