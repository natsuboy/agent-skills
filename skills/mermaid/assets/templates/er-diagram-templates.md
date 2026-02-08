# ER Diagram 模板库

本文档提供高质量的实体关系图模板，可直接复制使用。

---

## 模板1：简单实体关系（评分：85分）⭐⭐⭐⭐

**适用场景**：基础数据库设计、简单关系

```mermaid
%%{init: {'theme':'default'}}%%
erDiagram
    USER ||--o{ ORDER : places
    USER {
        int id PK
        string username
        string email
    }
    
    ORDER {
        int id PK
        int user_id FK
        date created_at
    }
```

---

## 模板2：电商系统数据库（评分：92分）⭐⭐⭐⭐⭐

**适用场景**：电商系统、订单管理、完整数据模型

```mermaid
%%{init: {'theme':'default'}}%%
erDiagram
    USER ||--o{ ORDER : places
    USER ||--o{ ADDRESS : has
    USER ||--o{ CART : owns
    USER {
        bigint id PK "主键"
        varchar username UK "用户名"
        varchar email UK "邮箱"
        varchar password_hash "密码哈希"
        varchar phone "手机号"
        tinyint status "状态"
        timestamp created_at "创建时间"
        timestamp updated_at "更新时间"
    }
    
    ADDRESS {
        bigint id PK
        bigint user_id FK
        varchar name "收货人"
        varchar phone "电话"
        varchar province "省"
        varchar city "市"
        varchar district "区"
        varchar detail "详细地址"
        boolean is_default "是否默认"
    }
    
    ORDER ||--o{ ORDER_ITEM : contains
    ORDER ||--o{ ADDRESS : ships_to
    ORDER {
        bigint id PK
        varchar order_no UK "订单号"
        bigint user_id FK
        bigint address_id FK
        decimal total_amount "总金额"
        decimal paid_amount "实付金额"
        varchar status "状态"
        varchar payment_method "支付方式"
        timestamp paid_at "支付时间"
        timestamp created_at "创建时间"
    }
    
    ORDER_ITEM }o--|| PRODUCT : references
    ORDER_ITEM {
        bigint id PK
        bigint order_id FK
        bigint product_id FK
        bigint sku_id FK
        int quantity "数量"
        decimal price "单价"
        decimal subtotal "小计"
    }
    
    PRODUCT ||--|{ PRODUCT_SKU : has
    PRODUCT }o--|| CATEGORY : belongs_to
    PRODUCT {
        bigint id PK
        varchar name "商品名"
        text description "描述"
        bigint category_id FK
        varchar status "状态"
        timestamp created_at
    }
    
    PRODUCT_SKU {
        bigint id PK
        bigint product_id FK
        varchar sku_code UK "SKU编码"
        decimal price "价格"
        int stock "库存"
        varchar attributes "属性JSON"
    }
    
    CATEGORY {
        bigint id PK
        varchar name "分类名"
        bigint parent_id FK "父分类"
        int sort_order "排序"
    }
    
    CART ||--o{ CART_ITEM : contains
    CART {
        bigint id PK
        bigint user_id FK,UK
    }
    
    CART_ITEM }o--|| PRODUCT_SKU : references
    CART_ITEM {
        bigint id PK
        bigint cart_id FK
        bigint sku_id FK
        int quantity
    }
```

---

## 模板3：用户权限系统（评分：90分）⭐⭐⭐⭐⭐

**适用场景**：RBAC权限、用户管理

```mermaid
%%{init: {'theme':'default'}}%%
erDiagram
    USER ||--o{ USER_ROLE : has
    USER {
        bigint id PK
        varchar username UK
        varchar email UK
        varchar password_hash
        boolean is_active
        timestamp last_login
        timestamp created_at
    }
    
    ROLE ||--o{ USER_ROLE : assigned_to
    ROLE ||--o{ ROLE_PERMISSION : has
    ROLE {
        bigint id PK
        varchar name UK
        varchar description
        boolean is_system
    }
    
    USER_ROLE {
        bigint id PK
        bigint user_id FK
        bigint role_id FK
        timestamp granted_at
        bigint granted_by FK
    }
    
    PERMISSION ||--o{ ROLE_PERMISSION : granted_to
    PERMISSION {
        bigint id PK
        varchar code UK "权限代码"
        varchar name "权限名称"
        varchar module "所属模块"
        varchar description
    }
    
    ROLE_PERMISSION {
        bigint id PK
        bigint role_id FK
        bigint permission_id FK
    }
    
    USER ||--o{ AUDIT_LOG : generates
    AUDIT_LOG {
        bigint id PK
        bigint user_id FK
        varchar action "操作类型"
        varchar resource "资源"
        varchar resource_id "资源ID"
        text details "详情JSON"
        varchar ip_address
        timestamp created_at
    }
```

---

## 模板4：内容管理系统（评分：88分）⭐⭐⭐⭐

**适用场景**：CMS、博客系统、内容平台

```mermaid
%%{init: {'theme':'default'}}%%
erDiagram
    USER ||--o{ ARTICLE : writes
    USER ||--o{ COMMENT : posts
    USER {
        bigint id PK
        varchar username
        varchar email
        varchar avatar_url
        text bio
    }
    
    ARTICLE ||--o{ COMMENT : has
    ARTICLE ||--o{ ARTICLE_TAG : has
    ARTICLE }o--|| CATEGORY : belongs_to
    ARTICLE {
        bigint id PK
        bigint author_id FK
        bigint category_id FK
        varchar title
        varchar slug UK
        text content
        text excerpt
        varchar cover_image
        varchar status
        int view_count
        timestamp published_at
        timestamp created_at
    }
    
    TAG ||--o{ ARTICLE_TAG : used_in
    TAG {
        bigint id PK
        varchar name UK
        varchar slug UK
    }
    
    ARTICLE_TAG {
        bigint article_id PK
        bigint tag_id PK
    }
    
    CATEGORY {
        bigint id PK
        varchar name
        varchar slug UK
        bigint parent_id FK
    }
    
    COMMENT ||--o{ COMMENT : replies_to
    COMMENT {
        bigint id PK
        bigint article_id FK
        bigint user_id FK
        bigint parent_id FK
        text content
        varchar status
        timestamp created_at
    }
```

---

## 模板5：社交网络（评分：87分）⭐⭐⭐⭐

**适用场景**：社交平台、关注关系

```mermaid
%%{init: {'theme':'default'}}%%
erDiagram
    USER ||--o{ POST : creates
    USER ||--o{ FOLLOW : follows
    USER ||--o{ FOLLOW : followed_by
    USER ||--o{ LIKE : gives
    USER {
        bigint id PK
        varchar username UK
        varchar display_name
        text bio
        varchar avatar_url
        int followers_count
        int following_count
    }
    
    POST ||--o{ LIKE : receives
    POST ||--o{ COMMENT : has
    POST ||--o{ POST_MEDIA : contains
    POST {
        bigint id PK
        bigint user_id FK
        text content
        int likes_count
        int comments_count
        int shares_count
        timestamp created_at
    }
    
    POST_MEDIA {
        bigint id PK
        bigint post_id FK
        varchar media_type
        varchar url
        int sort_order
    }
    
    FOLLOW {
        bigint id PK
        bigint follower_id FK
        bigint following_id FK
        timestamp created_at
    }
    
    LIKE {
        bigint id PK
        bigint user_id FK
        bigint post_id FK
        timestamp created_at
    }
    
    COMMENT {
        bigint id PK
        bigint post_id FK
        bigint user_id FK
        bigint reply_to_id FK
        text content
        timestamp created_at
    }
```

---

## 使用说明

### 关系符号

| 符号 | 说明 | 示例 |
|------|------|------|
| `\|\|` | 恰好一个 | 一 |
| `o\|` | 零或一个 | 零或一 |
| `}o` | 零或多个 | 多（可选） |
| `}\|` | 一或多个 | 多（必须） |

### 关系组合

```
||--||  一对一
||--o{  一对多
}o--o{  多对多
||--o|  一对零或一
||--|{  一对一或多个
```

### 实体定义

```mermaid
erDiagram
    ENTITY {
        type name PK "主键"
        type name FK "外键"
        type name UK "唯一键"
        type name    "普通字段"
    }
```

### 数据类型建议

| 类型 | 用途 |
|------|------|
| `bigint` | ID、外键 |
| `varchar` | 短文本 |
| `text` | 长文本 |
| `decimal` | 金额 |
| `int` | 整数 |
| `boolean` | 布尔值 |
| `timestamp` | 时间戳 |
| `date` | 日期 |

### 关系标签

```mermaid
erDiagram
    A ||--o{ B : "关系描述"
```
