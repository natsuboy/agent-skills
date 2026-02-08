# Agent Skills 清单

本文档列出了所有可用的 Agent Skills，包括其功能描述、使用方法和安装方式。

## 目录

- [Mermaid](#1-mermaid) - 专业的 Mermaid 图表生成 Skill

---

## 1. Mermaid

**版本**：v1.0.0

**描述**：专业的 Mermaid 图表生成 Skill，为 AI Agent 提供高质量、美观、语法正确的图表创建能力。支持 Dark 模式和自动验证。

**安装方式**：

```bash
# 使用 skills.sh CLI（推荐）
npx skills add natsuboy/agent-skills --skill mermaid

# 或手动安装
git clone https://github.com/natsuboy/agent-skills.git
cp -r agent-skills/skills/mermaid ~/.claude/skills/
```

**功能特性**：

- ✅ 支持所有 Mermaid v11+ 图表类型
- ✅ Dark 模式支持
- ✅ 自动语法验证
- ✅ 丰富的图表模板
- ✅ Agent 协作模式（通过 delegate_task）

**支持的图表类型**：

- Flowchart（流程图）
- Sequence Diagram（时序图）
- Class Diagram（类图）
- State Diagram（状态图）
- Gantt Chart（甘特图）
- Pie Chart（饼图）
- Mindmap（思维导图）
- ER Diagram（实体关系图）
- User Journey（用户旅程图）
- Timeline（时间线）
- Architecture Diagram（架构图）
- Kanban（看板）
- Requirement Diagram（需求图）

**使用示例**：

```
用户: 画一个 Mermaid 流程图展示用户注册流程
Agent: [自动委托给 mermaid skill 子 agent]
子 Agent: [生成并验证流程图代码]
```

**文档链接**：

- [详细文档](skills/mermaid/README.md)
- [GitHub Release](https://github.com/natsuboy/agent-skills/releases/tag/mermaid-v1.0.0)

---

## 安装所有 Skills

如果你想要安装所有可用的 Skills：

```bash
npx skills add natsuboy/agent-skills
```

---

## 贡献新 Skills

欢迎贡献新的 Skills！请参考以下文档：

- [开发规范](AGENTS.md)
- [项目 README](README.md)

创建新 Skill 的步骤：

1. 运行 `make create SKILL_NAME=my-new-skill`
2. 编辑 `SKILL.md` 定义功能
3. 实现必要的脚本和文档
4. 验证：`make validate SKILL_NAME=my-new-skill`
5. 预览：`make preview SKILL_NAME=my-new-skill`
6. 提交并发布：`make tag SKILL_NAME=my-new-skill VERSION=1.0.0`

---

## 问题反馈

如果你在使用 Skills 时遇到问题或有改进建议，请：

- 提交 [GitHub Issue](https://github.com/natsuboy/agent-skills/issues)
- 查看现有 Issues 寻找解决方案
- 参考 [常见问题](README.md#9-常见问题)

---

## 相关链接

- **GitHub 仓库**：https://github.com/natsuboy/agent-skills
- **skills.sh 生态**：https://skills.sh
- **开发规范**：[AGENTS.md](AGENTS.md)
- **项目主页**：[README.md](README.md)
