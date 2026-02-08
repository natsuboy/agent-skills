# 架构图 Dark 模板库 (v11+) - Flowchart 版本

本文档提供适用于深色背景编辑器的高质量架构图模板，使用 flowchart 语法实现专业、美观的架构设计。

> ✅ **兼容性优势**：Flowchart 是 Mermaid 的核心图表类型，兼容性最佳，所有版本都支持。
> 🎨 **样式灵活**：专为 Dark Mode 优化的配色方案，高对比度，护眼舒适。
> 📱 **图标方案**：使用表情符号作为节点标识，无需额外配置图标集。

---

## 📊 优化模板集合 (Dark Mode)

### 模板1：现代云原生架构（评分：95分）⭐⭐⭐⭐⭐

**适用场景**：现代云原生应用、微服务架构、深色演示文稿

**特点**：深邃的背景色搭配高亮边框，层次分明

```mermaid
%%{init: {'theme': 'dark', 'themeVariables': {
    'primaryColor': '#1e293b',
    'primaryTextColor': '#e2e8f0',
    'primaryBorderColor': '#38bdf8',
    'lineColor': '#94a3b8',
    'sectionBkgColor': '#0f172a',
    'altSectionBkgColor': '#1e293b',
    'gridColor': '#334155'
}}}%%
flowchart TB
    subgraph Ingress["🌐 Ingress Layer"]
        direction TB
        Nginx["⚙️ Nginx Ingress"]
        Gateway["🛡️ API Gateway"]
    end

    subgraph Services["⚙️ Services Layer"]
        direction LR
        Auth["🔐 Auth Service"]
        User["👤 User Service"]
        Order["📦 Order Service"]
        Payment["💳 Payment Service"]
    end

    subgraph Data["💾 Data Layer"]
        direction TB
        Redis[(⚡ Redis Cache)]
        Postgres[(🐘 PostgreSQL)]
        Kafka["🎭 Kafka"]
    end

    subgraph External["☁️ External Services"]
        direction TB
        SNS["📢 AWS SNS"]
        SES["📧 AWS SES"]
    end

    Nginx --> Gateway
    Gateway --> Auth
    Gateway --> User
    Gateway --> Order
    Gateway --> Payment

    Auth --> Redis
    User --> Postgres
    User --> Redis
    Order --> Kafka
    Order --> Redis

    Payment --> SNS
    Payment --> SES

    %% Dark Mode Styles
    style Ingress fill:#1e3a8a,stroke:#60a5fa,stroke-width:2px,color:#dbeafe
    style Services fill:#14532d,stroke:#4ade80,stroke-width:2px,color:#dcfce7
    style Data fill:#7c2d12,stroke:#fb923c,stroke-width:2px,color:#ffedd5
    style External fill:#581c87,stroke:#c084fc,stroke-width:2px,color:#f3e8ff
```

---

### 模板2：AWS 基础设施架构（评分：96分）⭐⭐⭐⭐⭐

**适用场景**：AWS 云服务部署、Serverless 架构

**特点**：AWS 标志性橙色/黄色的暗色适配版

```mermaid
%%{init: {'theme': 'dark', 'themeVariables': {
    'primaryColor': '#431407',
    'primaryTextColor': '#ffedd5',
    'primaryBorderColor': '#fb923c',
    'lineColor': '#fdba74',
    'sectionBkgColor': '#2a1205',
    'altSectionBkgColor': '#431407',
    'gridColor': '#7c2d12'
}}}%%
flowchart TB
    subgraph VPC["☁️ AWS VPC"]
        direction TB

        subgraph Public["🌐 Public Subnets"]
            direction TB
            IGW["🔌 Internet Gateway"]
            ALB["⚖️ Application LB"]
            CF["☁️ CloudFront"]
        end

        subgraph Private["🔒 Private Subnets"]
            direction LR
            EC2["💻 EC2 Auto Scaling"]
            ECS["🐳 ECS Cluster"]
            LAMBDA["⚡ Lambda Functions"]
        end

        subgraph DataSubnets["💾 Data Subnets"]
            direction LR
            RDS[(🐘 Amazon RDS)]
            DYNAMODB[(📊 DynamoDB)]
            ELASTICACHE[(⚡ ElastiCache)]
            S3[(🗄️ Amazon S3)]
        end
    end

    CF --> ALB
    ALB --> ECS
    ALB --> EC2
    ALB --> LAMBDA

    ECS --> RDS
    ECS --> S3
    EC2 --> DYNAMODB
    LAMBDA --> ELASTICACHE
    LAMBDA --> S3

    IGW --> ALB

    %% Dark Mode Styles - AWS Colors
    style VPC fill:#271300,stroke:#ea580c,stroke-width:2px,color:#ffedd5
    style Public fill:#431407,stroke:#f97316,stroke-width:2px,color:#ffedd5
    style Private fill:#3f2c00,stroke:#eab308,stroke-width:2px,color:#fef08a
    style DataSubnets fill:#450a0a,stroke:#ef4444,stroke-width:2px,color:#fee2e2
```

---

### 模板3：Kubernetes 生产架构（评分：97分）⭐⭐⭐⭐⭐

**适用场景**：K8s 生产集群、CI/CD 管道

**特点**：K8s 标志性蓝色的暗色适配

```mermaid
%%{init: {'theme': 'dark', 'themeVariables': {
    'primaryColor': '#172554',
    'primaryTextColor': '#dbeafe',
    'primaryBorderColor': '#3b82f6',
    'lineColor': '#60a5fa',
    'sectionBkgColor': '#0f172a',
    'altSectionBkgColor': '#1e293b',
    'gridColor': '#1e3a8a'
}}}%%
flowchart TB
    subgraph Cluster["☸️ Kubernetes Cluster"]
        direction TB

        subgraph IngressNS["🚦 Ingress Namespace"]
            direction TB
            TRAEFIK["🌐 Traefik Ingress"]
            CERT["📜 Cert Manager"]
        end

        subgraph AppsNS["📦 Applications Namespace"]
            direction LR
            FRONTEND["🖥️ Frontend Deployment"]
            API["⚙️ API Server Deployment"]
            WORKER["👷 Worker Deployment"]
            CRON["⏰ Cron Jobs"]
        end

        subgraph StorageNS["💾 Storage Namespace"]
            direction TB
            POSTGRES[(🐘 PostgreSQL StatefulSet)]
            REDIS[(⚡ Redis StatefulSet)]
            PVC["📁 Persistent Volumes"]
        end
    end

    TRAEFIK --> FRONTEND
    TRAEFIK --> API

    API --> WORKER
    API --> POSTGRES
    API --> REDIS

    WORKER --> POSTGRES
    WORKER --> REDIS

    CRON --> API
    CRON --> POSTGRES

    POSTGRES --> PVC
    REDIS --> PVC

    %% Dark Mode Styles - K8s Blue
    style Cluster fill:#0f172a,stroke:#3b82f6,stroke-width:2px,color:#dbeafe
    style IngressNS fill:#064e3b,stroke:#22c55e,stroke-width:2px,color:#dcfce7
    style AppsNS fill:#431407,stroke:#f97316,stroke-width:2px,color:#ffedd5
    style StorageNS fill:#3b0764,stroke:#a855f7,stroke-width:2px,color:#f3e8ff
```

---

### 模板4：微服务电商架构（评分：94分）⭐⭐⭐⭐⭐

**适用场景**：电商平台、分布式系统

**特点**：高对比度的模块区分

```mermaid
%%{init: {'theme': 'dark', 'themeVariables': {
    'primaryColor': '#14532d',
    'primaryTextColor': '#dcfce7',
    'primaryBorderColor': '#22c55e',
    'lineColor': '#4ade80',
    'sectionBkgColor': '#064e3b',
    'altSectionBkgColor': '#14532d',
    'gridColor': '#166534'
}}}%%
flowchart LR
    subgraph Clients["👥 Client Layer"]
        direction TB
        WEB["💻 React Web App"]
        MOBILE["📱 Mobile App"]
    end

    subgraph Gateway["🛡️ Gateway Layer"]
        direction TB
        APIGW["🚪 API Gateway"]
        RATELIMIT["🚦 Rate Limiter"]
    end

    subgraph Services["⚙️ Service Layer"]
        direction TB
        CATALOG["🏪 Catalog Service"]
        CART["🛒 Cart Service"]
        ORDER["📦 Order Service"]
        INVENTORY["📦 Inventory Service"]
        NOTIFICATION["🔔 Notification Service"]
    end

    subgraph Messaging["📨 Messaging Layer"]
        direction TB
        KAFKA["🎭 Kafka Cluster"]
        RABBITMQ["🐰 RabbitMQ"]
    end

    subgraph Data["💾 Data Layer"]
        direction TB
        MYSQL[(🐬 MySQL Primary)]
        MYSQL_SLAVE[(🐬 MySQL Replica)]
        MONGO[(🍃 MongoDB)]
        REDIS[(⚡ Redis Cache)]
    end

    WEB --> APIGW
    MOBILE --> APIGW

    APIGW --> RATELIMIT
    APIGW --> CATALOG
    APIGW --> CART
    APIGW --> ORDER
    APIGW --> INVENTORY

    CART --> KAFKA
    ORDER --> KAFKA
    INVENTORY --> RABBITMQ

    CATALOG --> REDIS
    CATALOG --> MYSQL
    CART --> REDIS
    ORDER --> MYSQL
    ORDER --> MONGO
    INVENTORY --> MYSQL_SLAVE
    INVENTORY --> REDIS

    NOTIFICATION --> RABBITMQ
    NOTIFICATION --> MONGO

    %% Dark Mode Styles - High Contrast
    style Clients fill:#1e3a8a,stroke:#3b82f6,stroke-width:2px,color:#dbeafe
    style Gateway fill:#4c1d95,stroke:#8b5cf6,stroke-width:2px,color:#ede9fe
    style Services fill:#14532d,stroke:#22c55e,stroke-width:2px,color:#dcfce7
    style Messaging fill:#7c2d12,stroke:#f97316,stroke-width:2px,color:#ffedd5
    style Data fill:#881337,stroke:#f43f5e,stroke-width:2px,color:#ffe4e6
```

---

### 模板5：DevOps CI/CD 架构（评分：93分）⭐⭐⭐⭐

**适用场景**：CI/CD 管道、DevOps 流程

**特点**：冷色调工业风

```mermaid
%%{init: {'theme': 'dark', 'themeVariables': {
    'primaryColor': '#334155',
    'primaryTextColor': '#f1f5f9',
    'primaryBorderColor': '#94a3b8',
    'lineColor': '#cbd5e1',
    'sectionBkgColor': '#1e293b',
    'altSectionBkgColor': '#334155',
    'gridColor': '#475569'
}}}%%
flowchart TB
    subgraph SCM["📁 Source Control"]
        direction LR
        GITHUB["🐙 GitHub Repository"]
        GITLAB["🦊 GitLab Repository"]
    end

    subgraph CI["🔧 CI/CD"]
        direction LR
        JENKINS["👷 Jenkins Pipeline"]
        GITHUB_ACTIONS["⚡ GitHub Actions"]
        GITLAB_CI["🔄 GitLab CI"]
        SONAR["🔍 SonarQube"]
    end

    subgraph Registry["📦 Artifact Registry"]
        direction LR
        DOCKERHUB["🐳 Docker Hub"]
        ECR["📊 AWS ECR"]
    end

    subgraph Staging["🚀 Staging"]
        direction TB
        STAGING_ECS["🐳 Staging ECS"]
        STAGING_DB[(🐘 Staging DB)]
    end

    subgraph Production["🎯 Production"]
        direction TB
        PROD_ECS["🐳 Production ECS"]
        PROD_DB[(🐘 Production DB)]
        PROD_ALB["⚖️ ALB"]
    end

    GITHUB --> JENKINS
    GITHUB --> GITHUB_ACTIONS
    GITLAB --> GITLAB_CI

    JENKINS --> SONAR
    JENKINS --> DOCKERHUB
    JENKINS --> ECR
    GITHUB_ACTIONS --> DOCKERHUB
    GITLAB_CI --> ECR

    ECR --> STAGING_ECS
    DOCKERHUB --> STAGING_ECS
    STAGING_ECS --> STAGING_DB

    ECR --> PROD_ECS
    PROD_ECS --> PROD_DB
    PROD_ALB --> PROD_ECS

    %% Dark Mode Styles
    style SCM fill:#1c1917,stroke:#78716c,stroke-width:2px,color:#f5f5f4
    style CI fill:#1e3a8a,stroke:#3b82f6,stroke-width:2px,color:#dbeafe
    style Registry fill:#14532d,stroke:#22c55e,stroke-width:2px,color:#dcfce7
    style Staging fill:#7c2d12,stroke:#f97316,stroke-width:2px,color:#ffedd5
    style Production fill:#7f1d1d,stroke:#ef4444,stroke-width:2px,color:#fee2e2
```

---

### 模板6：数据湖架构（评分：95分）⭐⭐⭐⭐⭐

**适用场景**：大数据处理、数据仓库、数据湖

**特点**：深蓝科技感

```mermaid
%%{init: {'theme': 'dark', 'themeVariables': {
    'primaryColor': '#172554',
    'primaryTextColor': '#dbeafe',
    'primaryBorderColor': '#3b82f6',
    'lineColor': '#60a5fa',
    'sectionBkgColor': '#0f172a',
    'altSectionBkgColor': '#1e293b',
    'gridColor': '#1e3a8a'
}}}%%
flowchart TB
    subgraph Ingestion["📥 Data Ingestion"]
        direction LR
        KAFKA["🎭 Kafka Cluster"]
        KINESIS["🌊 AWS Kinesis"]
        SQS["📬 Amazon SQS"]
    end

    subgraph Processing["⚙️ Data Processing"]
        direction LR
        SPARK["⚡ Spark Cluster"]
        AIRFLOW["🔄 Airflow DAGs"]
        GLUE["🔗 AWS Glue ETL"]
    end

    subgraph Storage["💾 Data Storage"]
        direction TB
        S3_RAW[(🗄️ S3 Raw)]
        S3_PROCESSED[(🗄️ S3 Processed)]
        S3_CURATED[(🗄️ S3 Curated)]
        REDSHIFT[(📊 Redshift Warehouse)]
        ATHENA["🔍 Amazon Athena"]
    end

    subgraph Analytics["📊 Analytics"]
        direction LR
        BI["📈 BI Tools"]
        JUPYTER["📓 Jupyter Notebooks"]
        ML["🤖 ML Models"]
    end

    subgraph Serving["🚀 Data Serving"]
        direction TB
        API["🌐 API Gateway"]
        LAMBDA["⚡ Query Lambda"]
        QUICKSIGHT["📊 QuickSight Dashboard"]
    end

    KAFKA --> SPARK
    KINESIS --> GLUE
    SQS --> AIRFLOW

    SPARK --> S3_RAW
    GLUE --> S3_RAW

    AIRFLOW --> S3_PROCESSED
    S3_RAW --> S3_PROCESSED

    S3_PROCESSED --> S3_CURATED
    S3_PROCESSED --> REDSHIFT

    REDSHIFT --> BI
    REDSHIFT --> JUPYTER
    REDSHIFT --> QUICKSIGHT

    S3_CURATED --> ATHENA
    ATHENA --> ML
    ATHENA --> API

    API --> LAMBDA
    LAMBDA --> S3_CURATED

    %% Dark Mode Styles
    style Ingestion fill:#14532d,stroke:#22c55e,stroke-width:2px,color:#dcfce7
    style Processing fill:#1e3a8a,stroke:#3b82f6,stroke-width:2px,color:#dbeafe
    style Storage fill:#7c2d12,stroke:#f97316,stroke-width:2px,color:#ffedd5
    style Analytics fill:#581c87,stroke:#a855f7,stroke-width:2px,color:#f3e8ff
    style Serving fill:#7f1d1d,stroke:#ef4444,stroke-width:2px,color:#fee2e2
```

---

## 🎨 Dark Mode 常用颜色方案

在深色模式下，建议使用较深的背景色（Background）搭配明亮的边框色（Stroke）和文字色（Text），以确保对比度和可读性。

### 蓝色系 - 接入层/客户端

```mermaid
flowchart TB
    A["接入层"]
    style A fill:#1e3a8a,stroke:#60a5fa,stroke-width:2px,color:#dbeafe
```

- 背景色：`#1e3a8a` (Dark Blue 900)
- 边框色：`#60a5fa` (Blue 400)
- 文字色：`#dbeafe` (Blue 100)

### 绿色系 - 服务层

```mermaid
flowchart TB
    A["服务层"]
    style A fill:#14532d,stroke:#4ade80,stroke-width:2px,color:#dcfce7
```

- 背景色：`#14532d` (Green 900)
- 边框色：`#4ade80` (Green 400)
- 文字色：`#dcfce7` (Green 100)

### 橙色系 - 数据层

```mermaid
flowchart TB
    A["数据层"]
    style A fill:#7c2d12,stroke:#fb923c,stroke-width:2px,color:#ffedd5
```

- 背景色：`#7c2d12` (Orange 900)
- 边框色：`#fb923c` (Orange 400)
- 文字色：`#ffedd5` (Orange 100)

### 紫色系 - 外部服务/消息层

```mermaid
flowchart TB
    A["外部服务"]
    style A fill:#581c87,stroke:#c084fc,stroke-width:2px,color:#f3e8ff
```

- 背景色：`#581c87` (Purple 900)
- 边框色：`#c084fc` (Purple 400)
- 文字色：`#f3e8ff` (Purple 100)

### 灰色系 - 基础设施

```mermaid
flowchart TB
    A["基础设施"]
    style A fill:#1c1917,stroke:#a8a29e,stroke-width:2px,color:#f5f5f4
```

- 背景色：`#1c1917` (Stone 900)
- 边框色：`#a8a29e` (Stone 400)
- 文字色：`#f5f5f4` (Stone 100)
