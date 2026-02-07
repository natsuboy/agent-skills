# Mermaid 图表类型完全指南

本指南详细介绍 Mermaid 支持的所有图表类型，包括语法、使用场景和完整示例。

## 0. 目录

1. [Flowchart - 流程图](#1-flowchart---流程图)
2. [Sequence Diagram - 时序图](#2-sequence-diagram---时序图)
3. [Class Diagram - 类图](#3-class-diagram---类图)
4. [State Diagram - 状态图](#4-state-diagram---状态图)
5. [Gantt - 甘特图](#5-gantt---甘特图)
6. [ER Diagram - 实体关系图](#6-er-diagram---实体关系图)
7. [User Journey - 用户旅程图](#7-user-journey---用户旅程图)
8. [Pie Chart - 饼图](#8-pie-chart---饼图)
9. [Mindmap - 思维导图](#9-mindmap---思维导图)
10. [Timeline - 时间线](#10-timeline---时间线)
11. [v11+新图表类型](#11-v11新图表类型)

---

## 1. Flowchart - 流程图

### 适用场景

- 系统架构图
- 业务流程
- 算法逻辑
- 决策树
- 数据流

### 基本语法

**声明和方向**：
```mermaid
flowchart TD    %% 从上到下
flowchart LR    %% 从左到右
flowchart RL    %% 从右到左
flowchart BT    %% 从下到上
```

**节点形状**：
```mermaid
flowchart LR
    A[矩形]
    B(圆角矩形)
    C([体育场形])
    D[[子程序]]
    E[(数据库)]
    F((圆形))
    G>不对称]
    H{菱形}
    I{{六边形}}
    J[/平行四边形/]
```

**连接线类型**：
```mermaid
flowchart LR
    A --> B       %% 箭头
    C --- D       %% 实线
    E -.- F       %% 虚线
    G ==> H       %% 粗箭头
    I --文字--> J  %% 带文字
    K -->|文字| L  %% 另一种带文字
```

### 完整示例

**系统架构图**：
```mermaid
%%{init: {'theme':'default'}}%%
flowchart TB
    subgraph clients[客户端]
        A([Web应用])
        B([移动应用])
    end
    
    subgraph gateway[网关层]
        C[Nginx]
        D[API Gateway]
    end
    
    subgraph services[微服务]
        E[认证服务]
        F[用户服务]
        G[订单服务]
    end
    
    subgraph data[数据层]
        H[(PostgreSQL)]
        I[(Redis)]
    end
    
    A --> C --> D
    B --> C
    D --> E & F & G
    E & F --> H
    F --> I
    G --> H
```

### 常见陷阱

1. **关键字冲突**：`end`、`class`、`click` 等需要用引号包裹
2. **特殊字符**：标签中的 `(){}[]` 需要用引号包裹
3. **废弃语法**：使用 `flowchart` 而非 `graph`

---

## 2. Sequence Diagram - 时序图

### 适用场景

- API 调用流程
- 对象间交互
- 协议通信
- 微服务调用链

### 基本语法

**参与者声明**：
```mermaid
sequenceDiagram
    participant A as 别名A
    actor B as 用户B
```

**消息类型**：
```mermaid
sequenceDiagram
    A->>B: 实线箭头
    A-->>B: 虚线箭头
    A-)B: 异步消息
    A-xB: 丢失消息
    A--)B: 虚线异步
```

**激活和注释**：
```mermaid
sequenceDiagram
    A->>+B: 请求（激活B）
    B-->>-A: 响应（停用B）
    Note over A,B: 这是注释
    Note right of B: 右侧注释
```

### 完整示例

**用户登录流程**：
```mermaid
%%{init: {'theme':'default'}}%%
sequenceDiagram
    actor User as 用户
    participant Web as Web应用
    participant API as API服务
    participant Auth as 认证服务
    participant DB as 数据库
    
    User->>Web: 输入用户名密码
    Web->>API: POST /login
    activate API
    
    API->>Auth: 验证凭证
    activate Auth
    Auth->>DB: 查询用户
    activate DB
    DB-->>Auth: 返回用户信息
    deactivate DB
    
    Auth->>Auth: 验证密码
    Auth-->>API: 返回Token
    deactivate Auth
    
    API-->>Web: 200 OK + Token
    deactivate API
    Web-->>User: 登录成功
    
    Note over User,DB: 整个流程约200ms
```

### 高级特性

**循环和条件**：
```mermaid
sequenceDiagram
    loop 每秒
        A->>B: 心跳检测
    end
    
    alt 成功
        B-->>A: 正常响应
    else 超时
        B--xA: 无响应
    end
    
    opt 可选操作
        A->>C: 记录日志
    end
```

---

## 3. Class Diagram - 类图

### 适用场景

- 面向对象设计
- 数据模型
- API 接口定义
- 领域模型

### 基本语法

```mermaid
classDiagram
    class Animal {
        +String name
        +int age
        +eat()
        +sleep()
    }
    
    class Dog {
        +bark()
    }
    
    Animal <|-- Dog : 继承
```

**关系类型**：
```
<|-- 继承
*-- 组合
o-- 聚合
--> 关联
-- 链接
..> 依赖
..|> 实现
```

### 完整示例

```mermaid
%%{init: {'theme':'default'}}%%
classDiagram
    class User {
        +Long id
        +String username
        +String email
        +login()
        +logout()
    }
    
    class Order {
        +Long id
        +Date createTime
        +Decimal amount
        +create()
        +cancel()
    }
    
    class Product {
        +Long id
        +String name
        +Decimal price
    }
    
    class OrderItem {
        +int quantity
        +Decimal subtotal
    }
    
    User "1" --> "*" Order : 创建
    Order "1" *-- "*" OrderItem : 包含
    OrderItem "*" --> "1" Product : 引用
```

---

## 4. State Diagram - 状态图

### 适用场景

- 状态机设计
- 工作流状态
- 生命周期管理
- 订单状态流转

### 基本语法

```mermaid
stateDiagram-v2
    [*] --> 待处理
    待处理 --> 处理中 : 开始处理
    处理中 --> 已完成 : 处理成功
    处理中 --> 失败 : 处理失败
    已完成 --> [*]
    失败 --> [*]
```

### 完整示例

**订单状态流转**：
```mermaid
%%{init: {'theme':'default'}}%%
stateDiagram-v2
    [*] --> 待支付
    
    待支付 --> 已支付 : 支付成功
    待支付 --> 已取消 : 用户取消
    待支付 --> 已取消 : 超时取消
    
    已支付 --> 待发货 : 确认订单
    已支付 --> 退款中 : 申请退款
    
    待发货 --> 已发货 : 发货
    待发货 --> 退款中 : 申请退款
    
    已发货 --> 已签收 : 确认收货
    已发货 --> 退货中 : 申请退货
    
    已签收 --> 已完成 : 确认完成
    已签收 --> 退货中 : 申请退货
    
    退款中 --> 已退款 : 退款成功
    退货中 --> 已退款 : 退货成功
    
    已完成 --> [*]
    已取消 --> [*]
    已退款 --> [*]
```

---

## 5. Gantt - 甘特图

### 适用场景

- 项目计划
- 任务排期
- 里程碑管理
- 资源分配

### 基本语法

```mermaid
gantt
    title 项目标题
    dateFormat YYYY-MM-DD
    
    section 阶段名称
    任务名称 :状态, id, 开始日期, 结束日期或持续时间
```

**任务状态**：
- `done` - 已完成
- `active` - 进行中
- `crit` - 关键任务
- 无状态 - 待开始

### 完整示例

```mermaid
%%{init: {'theme':'default'}}%%
gantt
    title 电商系统开发计划
    dateFormat YYYY-MM-DD
    
    section 需求阶段
    需求调研     :done, req1, 2026-01-01, 7d
    需求分析     :done, req2, after req1, 5d
    需求评审     :done, req3, after req2, 2d
    
    section 设计阶段
    架构设计     :done, des1, after req3, 5d
    数据库设计   :done, des2, after des1, 3d
    API设计      :active, des3, after des1, 4d
    UI设计       :active, des4, after req3, 10d
    
    section 开发阶段
    后端开发     :dev1, after des2, 20d
    前端开发     :dev2, after des4, 18d
    接口联调     :dev3, after dev1, 5d
    
    section 测试阶段
    单元测试     :test1, after dev1, 5d
    集成测试     :crit, test2, after dev3, 7d
    用户验收     :test3, after test2, 5d
    
    section 上线阶段
    部署上线     :crit, deploy, after test3, 2d
    监控观察     :monitor, after deploy, 7d
```

---

## 6. ER Diagram - 实体关系图

### 适用场景

- 数据库设计
- 数据模型
- 实体关系分析

### 基本语法

**关系符号**：
```
||--|| 一对一
||--o{ 一对多
}o--o{ 多对多
||--o| 一对零或一
```

### 完整示例

```mermaid
%%{init: {'theme':'default'}}%%
erDiagram
    USER ||--o{ ORDER : places
    USER {
        bigint id PK
        varchar username
        varchar email
        timestamp created_at
    }
    
    ORDER ||--|{ ORDER_ITEM : contains
    ORDER {
        bigint id PK
        bigint user_id FK
        decimal total_amount
        varchar status
        timestamp created_at
    }
    
    ORDER_ITEM }o--|| PRODUCT : references
    ORDER_ITEM {
        bigint id PK
        bigint order_id FK
        bigint product_id FK
        int quantity
        decimal price
    }
    
    PRODUCT {
        bigint id PK
        varchar name
        text description
        decimal price
        int stock
    }
    
    PRODUCT }o--|| CATEGORY : belongs_to
    CATEGORY {
        bigint id PK
        varchar name
        bigint parent_id FK
    }
```

---

## 7. User Journey - 用户旅程图

### 适用场景

- 用户体验分析
- 服务设计
- 流程优化

### 基本语法

```mermaid
journey
    title 旅程标题
    section 阶段名称
      任务描述: 评分: 参与者
```

### 完整示例

```mermaid
journey
    title 用户购物旅程
    
    section 发现商品
      浏览首页: 5: 用户
      搜索商品: 4: 用户
      查看详情: 5: 用户
      
    section 购买决策
      比较价格: 3: 用户
      查看评价: 4: 用户
      加入购物车: 5: 用户
      
    section 下单支付
      填写地址: 3: 用户
      选择支付: 4: 用户
      确认支付: 5: 用户, 支付系统
      
    section 收货评价
      等待发货: 3: 用户
      确认收货: 5: 用户
      发表评价: 4: 用户
```

---

## 8. Pie Chart - 饼图

### 适用场景

- 占比展示
- 数据分布
- 统计报告

### 基本语法

```mermaid
pie showData
    title 标题
    "项目A" : 30
    "项目B" : 25
    "项目C" : 45
```

### 完整示例

```mermaid
pie showData
    title 技术栈占比
    "TypeScript" : 40
    "Python" : 25
    "Go" : 20
    "Java" : 10
    "其他" : 5
```

---

## 9. Mindmap - 思维导图

### 适用场景

- 知识整理
- 头脑风暴
- 概念梳理

### 基本语法

```mermaid
mindmap
  root((中心主题))
    分支1
      子分支1.1
      子分支1.2
    分支2
      子分支2.1
```

### 完整示例

```mermaid
mindmap
  root((系统架构))
    前端
      Web应用
        React
        Vue
      移动应用
        iOS
        Android
    后端
      微服务
        用户服务
        订单服务
        支付服务
      网关
        Nginx
        Kong
    数据
      关系型
        PostgreSQL
        MySQL
      NoSQL
        Redis
        MongoDB
```

---

## 10. Timeline - 时间线

### 适用场景

- 历史事件
- 版本发布
- 项目里程碑

### 基本语法

```mermaid
timeline
    title 标题
    时间点1 : 事件描述
    时间点2 : 事件描述
```

### 完整示例

```mermaid
timeline
    title 产品发展历程
    
    2020 : 项目启动
         : 完成MVP开发
    
    2021 : 发布1.0版本
         : 用户突破1万
         : 获得A轮融资
    
    2022 : 发布2.0版本
         : 支持多语言
         : 用户突破10万
    
    2023 : 发布3.0版本
         : 引入AI功能
         : 获得B轮融资
```

---

## 11. v11+新图表类型

### Architecture Diagram 🔥

系统架构可视化，v11+新增。

```mermaid
architecture-beta
    group api(cloud)[API]

    service db(database)[Database] in api
    service disk1(disk)[Storage] in api
    service server(server)[Server] in api

    db:L -- R:server
    disk1:T -- B:server
```

### Kanban Board 🔥

看板图，v11+新增。

```mermaid
kanban
    Todo
        task1[任务1]
        task2[任务2]
    In Progress
        task3[任务3]
    Done
        task4[任务4]
```

### Block Diagram 🔥

块状图，v11+新增。

```mermaid
block-beta
    columns 3
    
    A["前端"]:1
    B["网关"]:1
    C["服务"]:1
    
    D["数据库"]:3
```

### XY Chart 🔥

坐标图，v11+新增。

```mermaid
xychart-beta
    title "月度销售额"
    x-axis [Jan, Feb, Mar, Apr, May]
    y-axis "销售额(万)" 0 --> 100
    bar [30, 45, 60, 55, 80]
    line [30, 45, 60, 55, 80]
```

---

## 12. 图表类型选择指南

| 需求 | 推荐类型 | 备选类型 |
|------|----------|----------|
| 系统架构 | Flowchart | Architecture |
| API调用流程 | Sequence Diagram | Flowchart |
| 数据模型 | ER Diagram | Class Diagram |
| 状态流转 | State Diagram | Flowchart |
| 项目计划 | Gantt | Timeline |
| 用户体验 | User Journey | Flowchart |
| 知识整理 | Mindmap | Flowchart |
| 数据占比 | Pie Chart | XY Chart |
| 任务管理 | Kanban | Gantt |
