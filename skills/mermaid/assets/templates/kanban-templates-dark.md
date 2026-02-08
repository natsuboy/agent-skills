# Kanban Dark 模板库 (v11+)

本文档提供适用于深色背景编辑器的 Mermaid Kanban 模板。

**注意**：Kanban 是 Mermaid v11+ 新增的实验性功能。

**适用场景**：
- Dark 模式编辑器
- 深色背景仪表板

---

## 模板1：敏捷软件开发看板 (Dark)（评分：95分）⭐⭐⭐⭐⭐

```mermaid
%%{init: {'theme': 'dark'}}%%
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

---

## 模板2：个人任务管理 (Dark)（评分：92分）⭐⭐⭐⭐

```mermaid
%%{init: {'theme': 'dark'}}%%
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

---

## 模板3：内容发布工作流 (Dark)（评分：90分）⭐⭐⭐⭐

```mermaid
%%{init: {'theme': 'dark'}}%%
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

---

## 模板4：缺陷追踪看板 (Dark)（评分：88分）⭐⭐⭐⭐

```mermaid
%%{init: {'theme': 'dark'}}%%
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
