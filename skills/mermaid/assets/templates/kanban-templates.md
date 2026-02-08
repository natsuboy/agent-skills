# Kanban 模板库 (v11+)

本文档提供 Mermaid Kanban (看板) 的标准模板，用于敏捷开发、任务管理和工作流可视化。

**注意**：Kanban 是 Mermaid v11+ 新增的实验性功能，请确保您的环境支持该版本。

**适用场景**：
- 敏捷软件开发 (Scrum/Kanban)
- 个人任务管理
- 内容发布流水线
- 问题/缺陷追踪

---

## 模板1：敏捷软件开发看板（评分：95分）⭐⭐⭐⭐⭐

**适用场景**：软件研发团队、Sprint管理

```mermaid
kanban
  Todo
    [登录页面设计]
    [数据库Schema定义]
    [API接口文档编写]
  In Progress
    [前端组件开发]
    [后端鉴权逻辑]
  Review
    [代码审查 PR#102]
    [UI走查]
  Testing
    [单元测试]
    [集成测试]
  Done
    [需求调研]
    [技术选型]
```

**特点**：
- 典型的软件开发流程列
- 简洁的任务卡片

---

## 模板2：个人任务管理（评分：92分）⭐⭐⭐⭐

**适用场景**：GTD (Getting Things Done)、个人计划

```mermaid
kanban
  Backlog
    [阅读《系统设计面试》]
    [学习 Rust]
    [整理书房]
  This Week
    [完成周报]
    [修复 Bug #123]
    [预约体检]
  Today
    [参加早会]
    [提交代码]
  Done
    [回复邮件]
    [缴纳电费]
```

**特点**：
- 按照时间维度划分（本周、今天）
- 适合个人日常管理

---

## 模板3：内容发布工作流（评分：90分）⭐⭐⭐⭐

**适用场景**：博客、媒体运营、内容创作

```mermaid
kanban
  Ideas
    [关于AI的未来]
    [Mermaid教程系列]
  Drafting
    [React性能优化指南]
  Editing
    [前端趋势报告2024]
  Scheduled
    [周五：技术周刊]
  Published
    [Docker入门指南]
    [Python爬虫实战]
```

**特点**：
- 反映了内容从创意到发布的完整生命周期

---

## 模板4：缺陷追踪看板（评分：88分）⭐⭐⭐⭐

**适用场景**：QA测试、Bug修复、工单管理

```mermaid
kanban
  New Issues
    id:1 [登录超时错误]
    id:2 [图片加载失败]
  Triaged
    id:3 [支付接口返回500]
  Fixing
    id:4 [样式兼容性问题]
  Verified
    id:5 [错别字修正]
  Closed
    id:6 [重复的提交]
```

**特点**：
- 包含 ID 标识（虽然目前 Kanban 语法对元数据的显示支持有限，但结构上可以模拟）

---

## 语法参考

### 基本结构
```mermaid
kanban
  列名称1
    [卡片内容1]
    [卡片内容2]
  列名称2
    [卡片内容3]
```

### 样式说明
目前 Mermaid Kanban 的样式定制能力相对较弱，主要依赖主题 (Theme) 进行自动着色。建议使用简洁的文本描述。
