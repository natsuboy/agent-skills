# Flowchart Dark 模板库

本文档提供适用于深色背景编辑器的高质量 Flowchart 模板，可直接复制使用。

**使用场景**：
- Dark 模式编辑器（如 VS Code Dark、JetBrains Darcula 等）
- 演示文稿中的深色幻灯片
- 深色主题的博客或文档网站

---

## 模板1：简单流程（评分：88分）⭐⭐⭐⭐

**适用场景**：基础流程、简单逻辑、快速草图

```mermaid
%%{init: {'theme':'dark'}}%%
flowchart LR
    A([开始]) --> B{判断条件}
    B -->|是| C[执行操作A]
    B -->|否| D[执行操作B]
    C --> E([结束])
    D --> E
    
    style A fill:#4dabf7,stroke:#1864ab,color:#fff
    style E fill:#4dabf7,stroke:#1864ab,color:#fff
    style B fill:#ffd43b,stroke:#f08c00,color:#212529
```

**视觉特点**：
- ✅ 使用 dark 主题（深色背景适配）
- ✅ 高对比度配色（文字使用白色/浅色）
- ✅ 起止点使用体育场形
- ✅ 判断使用菱形

---

## 模板2：系统架构图（评分：93分）⭐⭐⭐⭐⭐

**适用场景**：Web应用架构、分层系统、微服务架构

```mermaid
%%{init: {'theme':'dark'}}%%
flowchart TB
    subgraph clients[🌐 客户端]
        direction LR
        A([Web应用])
        B([移动应用])
    end
    
    subgraph gateway[🚪 网关层]
        C[Nginx]
        D[API Gateway]
    end
    
    subgraph services[⚙️ 微服务]
        direction LR
        E[认证服务]
        F[用户服务]
        G[订单服务]
    end
    
    subgraph data[💾 数据层]
        direction LR
        H[(PostgreSQL)]
        I[(Redis)]
    end
    
    A --> C
    B --> C
    C --> D
    D --> E & F & G
    E --> H
    F --> H & I
    G --> H
    
    style clients fill:#4dabf7,stroke:#1864ab,color:#fff
    style gateway fill:#ffa94d,stroke:#e67700,color:#212529
    style services fill:#da77f2,stroke:#9c36b5,color:#fff
    style data fill:#69db7c,stroke:#2b8a3e,color:#212529
```

**视觉特点**：
- ✅ 使用 dark 主题，深色背景适配
- ✅ 高对比度分层配色
- ✅ 每层使用 emoji 增强识别
- ✅ 文字使用白色/深色确保可读性
- ✅ 数据库使用圆柱形，端点使用体育场形

---

## 模板3：CI/CD流水线（评分：89分）⭐⭐⭐⭐

**适用场景**：DevOps流程、自动化部署、发布流程

```mermaid
%%{init: {'theme':'dark'}}%%
flowchart LR
    A([代码提交]) --> B[代码检查]
    B --> C[单元测试]
    C --> D{测试通过?}
    
    D -->|是| E[构建镜像]
    D -->|否| F[通知开发者]
    F --> A
    
    E --> G[推送镜像]
    G --> H[部署测试]
    H --> I[集成测试]
    I --> J{测试通过?}
    
    J -->|是| K[部署生产]
    J -->|否| F
    
    K --> L([上线完成])
    
    style A fill:#4dabf7,stroke:#1864ab,color:#fff
    style L fill:#69db7c,stroke:#2b8a3e,color:#212529
    style F fill:#ff8787,stroke:#c92a2a,color:#fff
    style K fill:#ffd43b,stroke:#f08c00,color:#212529
```

**视觉特点**：
- ✅ 使用 dark 主题
- ✅ 高对比度状态颜色（成功绿、失败红、关键黄）
- ✅ 使用 LR 方向（符合流程阅读习惯）
- ✅ 判断节点使用菱形

---

## 模板4：决策树（评分：86分）⭐⭐⭐⭐

**适用场景**：业务规则、条件判断、分类逻辑

```mermaid
%%{init: {'theme':'dark'}}%%
flowchart TD
    start([用户请求]) --> check1{用户已登录?}
    
    check1 -->|是| check2{有权限?}
    check1 -->|否| login[跳转登录]
    login --> start
    
    check2 -->|是| check3{资源存在?}
    check2 -->|否| denied[权限不足]
    
    check3 -->|是| success[返回资源]
    check3 -->|否| notfound[资源不存在]
    
    success --> done([请求完成])
    denied --> done
    notfound --> done
    
    style start fill:#4dabf7,stroke:#1864ab,color:#fff
    style done fill:#4dabf7,stroke:#1864ab,color:#fff
    style success fill:#69db7c,stroke:#2b8a3e,color:#212529
    style denied fill:#ff8787,stroke:#c92a2a,color:#fff
    style notfound fill:#ffd43b,stroke:#f08c00,color:#212529
```

---

## 模板5：数据流图（评分：87分）⭐⭐⭐⭐

**适用场景**：ETL流程、数据处理、数据管道

```mermaid
%%{init: {'theme':'dark'}}%%
flowchart LR
    subgraph source[📥 数据源]
        A[(MySQL)]
        B[(MongoDB)]
        C[/API接口/]
    end
    
    subgraph process[⚙️ 处理层]
        D[数据抽取]
        E[数据清洗]
        F[数据转换]
    end
    
    subgraph target[📤 目标]
        G[(数据仓库)]
        H[/BI报表/]
    end
    
    A --> D
    B --> D
    C --> D
    D --> E --> F
    F --> G --> H
    
    style source fill:#4dabf7,stroke:#1864ab,color:#fff
    style process fill:#ffa94d,stroke:#e67700,color:#212529
    style target fill:#69db7c,stroke:#2b8a3e,color:#212529
```

---

## 模板6：错误处理流程（评分：88分）⭐⭐⭐⭐

**适用场景**：异常处理、重试逻辑、降级策略

```mermaid
%%{init: {'theme':'dark'}}%%
flowchart TD
    A([接收请求]) --> B[处理请求]
    B --> C{处理成功?}
    
    C -->|是| D[返回结果]
    C -->|否| E{重试次数<3?}
    
    E -->|是| F[等待重试]
    F --> B
    E -->|否| G{启用降级?}
    
    G -->|是| H[降级处理]
    G -->|否| I[返回错误]
    
    H --> D
    D --> J([响应完成])
    I --> J
    
    style A fill:#4dabf7,stroke:#1864ab,color:#fff
    style J fill:#4dabf7,stroke:#1864ab,color:#fff
    style D fill:#69db7c,stroke:#2b8a3e,color:#212529
    style I fill:#ff8787,stroke:#c92a2a,color:#fff
    style H fill:#ffd43b,stroke:#f08c00,color:#212529
```

---

## 模板7：用户注册流程（评分：86分）⭐⭐⭐⭐

**适用场景**：用户流程、表单处理、验证逻辑

```mermaid
%%{init: {'theme':'dark'}}%%
flowchart TD
    A([开始注册]) --> B[填写表单]
    B --> C{表单有效?}
    
    C -->|否| D[显示错误]
    D --> B
    
    C -->|是| E{用户名存在?}
    E -->|是| F[提示重名]
    F --> B
    
    E -->|否| G[创建用户]
    G --> H[发送验证邮件]
    H --> I{邮件验证?}
    
    I -->|是| J[激活账户]
    I -->|超时| K[重发邮件]
    K --> I
    
    J --> L([注册成功])
    
    style A fill:#4dabf7,stroke:#1864ab,color:#fff
    style L fill:#69db7c,stroke:#2b8a3e,color:#212529
```

---

## 使用说明

### 如何使用模板

1. **复制模板代码**
2. **替换占位内容**：修改节点标签为实际内容
3. **调整结构**：根据需要增删节点和连接
4. **优化样式**：调整颜色和布局
5. **验证语法**：运行 `validate_mermaid.py`

### 切换主题

**切换到浅色主题**：
```text
%%{init: {'theme':'default'}}%%  %% 改为浅色主题
```

**切换到 forest 主题**：
```text
%%{init: {'theme':'forest'}}%%  %% 改为森林主题
```

### Dark 主题配色建议

**高对比度配色方案**：

| 用途 | 推荐颜色 | 文字颜色 |
|------|----------|----------|
| 蓝色系 | `#4dabf7`（浅蓝） | `#fff`（白色） |
| 绿色系 | `#69db7c`（浅绿） | `#212529`（深色） |
| 黄色系 | `#ffd43b`（浅黄） | `#212529`（深色） |
| 红色系 | `#ff8787`（浅红） | `#fff`（白色） |
| 紫色系 | `#da77f2`（浅紫） | `#fff`（白色） |
| 橙色系 | `#ffa94d`（浅橙） | `#212529`（深色） |

**配色原则**：
- 浅色背景节点 → 使用白色文字 `color:#fff`
- 深色/中性背景节点 → 使用深色文字 `color:#212529`
- 确保对比度至少 4.5:1（WCAG AA 标准）

### 自定义样式

**修改方向**：
```mermaid
%% 改为从左到右
flowchart LR
    A --> B
```

**添加更多样式**：
```mermaid
flowchart TD
    A[节点ID]
    style A fill:#4dabf7,stroke:#1864ab,stroke-width:3px,color:#fff
```

**使用 classDef 批量定义**：
```mermaid
flowchart TD
    classDef important fill:#ff8787,stroke:#c92a2a,color:#fff
    classDef success fill:#69db7c,stroke:#2b8a3e,color:#212529

    A[节点A]:::important
    B[节点B]:::success
```
