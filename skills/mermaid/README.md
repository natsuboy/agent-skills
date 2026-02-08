# 🎨 Mermaid Skill for AI Agents

专业的 Mermaid 图表生成 Skill，为 AI Agent 提供高质量、美观、语法正确的图表创建能力。

## ✨ 特性

- ✅ **86 个高质量模板** - 覆盖 7 种常用图表类型（包含 Dark Mode 适配版）
- ✅ **语法自动验证** - 确保生成的图表可渲染
- ✅ **视觉质量评分** - 自动评估美观度（目标 ≥80 分）
- ✅ **Mermaid v11+ 支持** - 支持 Architecture、Kanban 等新图表
- ✅ **独立子 Agent 执行** - 节省主对话 token，支持并行生成

## 📦 安装

```bash
# 自动安装
npx mermaid-skill-installer
```

## 🚀 快速使用

安装后，Agent 将具备以下能力：

> **用户**: "画一个电商系统的架构图"
>
> **Agent**: (自动调用 mermaid skill)
> 1. 选择 Architecture 模板
> 2. 生成 Mermaid 代码
> 3. 运行 `validate_mermaid.py` 验证语法和美观度
> 4. 返回高质量图表代码

## 🔧 包含内容

本 Skill 包含以下核心组件：

1.  **`SKILL.md`**: Agent 的核心指令集（Prompt、思维链、Few-Shot）。
2.  **`scripts/validate_mermaid.py`**: 自动验证脚本，用于检查语法和评分。
3.  **`assets/templates/`**: 包含 42 个经过优化的图表模板。
4.  **`references/`**: 包含最佳实践、配色指南和语法速查。

## 📊 质量指标

| 指标 | 目标 | 说明 |
|------|------|------|
| **语法正确性** | 100% | 必须通过 mermaid-cli 预渲染验证 |
| **视觉评分** | ≥80 | 基于节点布局、标签长度、主题配置评分 |
| **复杂度控制** | <20 节点 | 自动拆分复杂图表，避免混乱 |

## 🔗 相关资源

- [Mermaid 官方文档](https://mermaid.js.org/)
- [Mermaid Live Editor](https://mermaid.live/)
- [问题反馈](https://github.com/YOUR_USERNAME/agent-skills/issues)

---

**详细指令**: 请查看内部文档 [`SKILL.md`](SKILL.md)
