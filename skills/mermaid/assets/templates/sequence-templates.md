# Sequence Diagram 模板库

本文档提供高质量的时序图模板，可直接复制使用。

---

## 模板1：基础API调用（评分：85分）⭐⭐⭐⭐

**适用场景**：简单API请求、客户端-服务端交互

```mermaid
%%{init: {'theme':'default'}}%%
sequenceDiagram
    participant C as 客户端
    participant S as 服务端
    
    C->>S: 发送请求
    activate S
    S-->>C: 返回响应
    deactivate S
```

---

## 模板2：用户登录流程（评分：92分）⭐⭐⭐⭐⭐

**适用场景**：认证流程、JWT验证、OAuth

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
    DB-->>Auth: 用户信息
    deactivate DB
    
    Auth->>Auth: 验证密码
    
    alt 验证成功
        Auth-->>API: 生成Token
        API-->>Web: 200 OK + Token
        Web-->>User: 登录成功
    else 验证失败
        Auth-->>API: 验证失败
        API-->>Web: 401 Unauthorized
        Web-->>User: 登录失败
    end
    
    deactivate Auth
    deactivate API
    
    Note over User,DB: 整个流程约200ms
```

---

## 模板3：微服务调用链（评分：90分）⭐⭐⭐⭐⭐

**适用场景**：微服务通信、服务编排、分布式系统

```mermaid
%%{init: {'theme':'default'}}%%
sequenceDiagram
    participant GW as API网关
    participant US as 用户服务
    participant OS as 订单服务
    participant PS as 支付服务
    participant MQ as 消息队列
    participant NS as 通知服务
    
    GW->>US: 获取用户信息
    activate US
    US-->>GW: 用户数据
    deactivate US
    
    GW->>OS: 创建订单
    activate OS
    OS->>PS: 发起支付
    activate PS
    PS-->>OS: 支付结果
    deactivate PS
    
    OS-)MQ: 发送订单事件
    OS-->>GW: 订单创建成功
    deactivate OS
    
    MQ-)NS: 消费事件
    activate NS
    NS-->>NS: 发送通知
    deactivate NS
```

---

## 模板4：数据库事务（评分：88分）⭐⭐⭐⭐

**适用场景**：事务处理、数据一致性、ACID操作

```mermaid
%%{init: {'theme':'default'}}%%
sequenceDiagram
    participant App as 应用
    participant DB as 数据库
    
    App->>DB: BEGIN TRANSACTION
    activate DB
    
    App->>DB: INSERT 订单
    DB-->>App: OK
    
    App->>DB: UPDATE 库存
    
    alt 库存充足
        DB-->>App: OK
        App->>DB: COMMIT
        DB-->>App: 事务提交成功
    else 库存不足
        DB-->>App: ERROR
        App->>DB: ROLLBACK
        DB-->>App: 事务回滚
    end
    
    deactivate DB
```

---

## 模板5：OAuth2授权流程（评分：90分）⭐⭐⭐⭐⭐

**适用场景**：第三方登录、OAuth2、SSO

```mermaid
%%{init: {'theme':'default'}}%%
sequenceDiagram
    actor User as 用户
    participant App as 客户端应用
    participant Auth as 授权服务器
    participant Res as 资源服务器
    
    User->>App: 点击登录
    App->>Auth: 重定向到授权页面
    Auth->>User: 显示授权页面
    User->>Auth: 同意授权
    
    Auth->>App: 返回授权码
    App->>Auth: 用授权码换Token
    activate Auth
    Auth-->>App: 返回Access Token
    deactivate Auth
    
    App->>Res: 携带Token请求资源
    activate Res
    Res->>Auth: 验证Token
    Auth-->>Res: Token有效
    Res-->>App: 返回资源
    deactivate Res
    
    App-->>User: 显示资源
```

---

## 模板6：WebSocket通信（评分：86分）⭐⭐⭐⭐

**适用场景**：实时通信、推送消息、长连接

```mermaid
%%{init: {'theme':'default'}}%%
sequenceDiagram
    participant C as 客户端
    participant S as 服务器
    
    C->>S: 建立WebSocket连接
    S-->>C: 连接确认
    
    loop 心跳检测
        C->>S: ping
        S-->>C: pong
    end
    
    par 消息推送
        S-)C: 推送消息A
    and
        S-)C: 推送消息B
    end
    
    C->>S: 发送消息
    S-->>C: 消息确认
    
    C->>S: 关闭连接
    S-->>C: 关闭确认
```

---

## 模板7：异步消息处理（评分：87分）⭐⭐⭐⭐

**适用场景**：消息队列、异步处理、事件驱动

```mermaid
%%{init: {'theme':'default'}}%%
sequenceDiagram
    participant P as 生产者
    participant MQ as 消息队列
    participant C1 as 消费者1
    participant C2 as 消费者2
    
    P-)MQ: 发送消息
    Note right of MQ: 消息入队
    
    par 并行消费
        MQ-)C1: 投递消息
        activate C1
        C1-->>C1: 处理消息
        C1-)MQ: ACK确认
        deactivate C1
    and
        MQ-)C2: 投递消息
        activate C2
        C2-->>C2: 处理消息
        C2-)MQ: ACK确认
        deactivate C2
    end
```

---

## 使用说明

### 消息类型说明

| 语法 | 说明 | 使用场景 |
|------|------|----------|
| `->>` | 实线箭头 | 同步请求 |
| `-->>` | 虚线箭头 | 同步响应 |
| `-)` | 开放箭头 | 异步消息 |
| `--)` | 虚线开放 | 异步响应 |
| `-x` | 带×箭头 | 丢失消息 |

### 激活框使用

```mermaid
sequenceDiagram
    A->>+B: 请求（激活B）
    B-->>-A: 响应（停用B）
```

### 逻辑块

```mermaid
sequenceDiagram
    alt 条件1
        A->>B: 消息1
    else 条件2
        A->>B: 消息2
    end
    
    opt 可选
        A->>B: 可选消息
    end
    
    loop 循环条件
        A->>B: 重复消息
    end
    
    par 并行1
        A->>B: 消息A
    and 并行2
        A->>C: 消息B
    end
```
