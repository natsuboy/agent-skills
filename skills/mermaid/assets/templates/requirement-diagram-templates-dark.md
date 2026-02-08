# Requirement Diagram Dark 模板库

本文档提供适用于深色背景编辑器的 Mermaid Requirement Diagram 模板。

**适用场景**：
- Dark 模式编辑器
- 深色背景技术文档

---

## 模板1：软件功能需求 (Dark)（评分：92分）⭐⭐⭐⭐

```mermaid
%%{init: {'theme': 'dark'}}%%
requirementDiagram

    requirement test_req {
    id: 1
    text: "用户登录功能"
    risk: High
    verifymethod: test
    }

    element test_suite {
    type: simulation
    }

    test_suite - verifies -> test_req
```

---

## 模板2：性能与约束需求 (Dark)（评分：90分）⭐⭐⭐⭐

```mermaid
%%{init: {'theme': 'dark'}}%%
requirementDiagram

    requirement performance_req {
    id: 2
    text: "系统响应时间 < 200ms"
    risk: Medium
    verifymethod: test
    }

    requirement hardware_req {
    id: 3
    text: "必须运行在 Linux x86_64"
    risk: Low
    verifymethod: inspection
    }

    element benchmark_tool {
    type: tool
    }

    benchmark_tool - verifies -> performance_req
```

---

## 模板3：层级需求结构 (Dark)（评分：94分）⭐⭐⭐⭐⭐

```mermaid
%%{init: {'theme': 'dark'}}%%
requirementDiagram

    requirement system_req {
    id: 100
    text: "完整的电商系统"
    risk: High
    verifymethod: demonstration
    }

    requirement frontend_req {
    id: 101
    text: "响应式Web界面"
    risk: Medium
    verifymethod: test
    }

    requirement backend_req {
    id: 102
    text: "高并发API服务"
    risk: High
    verifymethod: test
    }

    system_req - contains -> frontend_req
    system_req - contains -> backend_req
```

---

## 模板4：安全合规需求 (Dark)（评分：91分）⭐⭐⭐⭐

```mermaid
%%{init: {'theme': 'dark'}}%%
requirementDiagram

    requirement security_req {
    id: 10
    text: "数据传输必须加密 (TLS 1.3)"
    risk: High
    verifymethod: Analysis
    }

    requirement gdpr_req {
    id: 11
    text: "符合 GDPR 隐私规范"
    risk: High
    verifymethod: Inspection
    }

    element security_audit {
    type: process
    }

    security_audit - satisfies -> security_req
    security_audit - satisfies -> gdpr_req
```
