# Agent Skills

我的 Agent Skills 集合，采用模块化结构组织，便于开发和发布。

## 📂 项目结构

- **`skills/`**: 包含所有 skill 实现。每个子目录都是一个独立的 skill。
- **`scripts/`**: 通用管理工具。
  - `init.sh`: 初始化仓库并替换占位符（如用户名、作者信息）。
  - `create_skill.sh`: 快速生成新 skill 的脚手架。
  - `publish.sh`: 构建和打包 skills。
- **`skills.json`**: 所有 skills 的中央配置注册表。

## 📦 可用 Skills

| Skill | 描述 | 状态 |
|-------|------|------|
| **[mermaid](skills/mermaid/README.md)** | 专为 AI Agent 设计的专业 Mermaid 图表生成 skill。 | ✅ Active |

## 🚀 快速开始

### 1. 初始化仓库 (只需一次)

如果你刚克隆了这个仓库，运行此命令来设置你的作者信息：

```bash
./scripts/init.sh
```

### 2. 创建新 Skill

无需手动复制文件，使用脚手架快速开始：

```bash
# 用法: ./scripts/create_skill.sh <skill-name>
./scripts/create_skill.sh my-new-skill
```

这会自动：
- 创建 `skills/my-new-skill` 目录结构
- 生成基础文档（SKILL.md, README.md）
- 在 `skills.json` 中注册新 skill

### 3. 发布 Skill

当你准备好发布时（生成 release 包和 npm 安装器）：

```bash
# 用法: ./scripts/publish.sh <skill-name> <version>
./scripts/publish.sh mermaid 1.0.0
```

**发布流程**：
1. **构建**：脚本会在 `build/mermaid/` 生成 `.tar.gz` 包和 npm 安装器。
2. **Git 发布**：提交代码并打上标签（如 `mermaid-v1.0.0`）。
   - *提示：GitHub Actions 已配置，推送到 GitHub 后会自动创建 Release。*
3. **NPM 发布**：进入 `build/mermaid/installer` 运行 `npm publish`。

## 📖 文档

- [Mermaid Skill 说明](skills/mermaid/README.md)
