# Requirement Diagram 模板库

本文档提供 Mermaid Requirement Diagram (需求图) 的标准模板，用于系统工程、需求管理和追踪。

**适用场景**：
- 系统需求规格说明 (SRS)
- 需求验证与测试覆盖
- 硬件/软件约束定义
- 复杂系统设计

---

## 模板1：软件功能需求（评分：92分）⭐⭐⭐⭐

**适用场景**：软件开发、功能定义

```mermaid
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

**特点**：
- 定义了具体需求
- 关联了验证方法（测试套件）

---

## 模板2：性能与约束需求（评分：90分）⭐⭐⭐⭐

**适用场景**：非功能性需求、性能指标

```mermaid
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

**特点**：
- 定义了性能指标和硬件约束
- 明确了验证手段（测量、检查）

---

## 模板3：层级需求结构（评分：94分）⭐⭐⭐⭐⭐

**适用场景**：复杂系统、需求分解

```mermaid
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

**特点**：
- 展示了需求之间的父子关系（contains）
- 适合顶层设计

---

## 模板4：安全合规需求（评分：91分）⭐⭐⭐⭐

**适用场景**：安全审计、合规性检查

```mermaid
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

**特点**：
- 明确了合规性需求
- 定义了关键风险等级 (High)

---

## 语法参考

### 关系类型
- **contains**: 包含关系
- **copies**: 复制关系
- **derives**: 衍生关系
- **satisfies**: 满足关系
- **verifies**: 验证关系
- **refines**: 细化关系
- **traces**: 追踪关系

### 验证方法 (verifymethod)
- **analysis**: 分析
- **inspection**: 检查
- **test**: 测试
- **demonstration**: 演示
