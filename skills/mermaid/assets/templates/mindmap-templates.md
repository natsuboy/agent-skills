# Mindmap 模板库

本文档提供 Mermaid Mindmap (思维导图) 的标准模板，用于头脑风暴、知识组织和结构化规划。

**适用场景**：
- 创意头脑风暴
- 组织架构展示
- 技术栈规划
- 课程/知识大纲

---

## 模板1：产品功能规划（评分：96分）⭐⭐⭐⭐⭐

**适用场景**：产品管理、需求梳理、功能设计

```mermaid
mindmap
  root((电商APP))
    用户端
      首页
        Banner推荐
        每日秒杀
        猜你喜欢
      商品详情
        图片轮播
        规格选择
        用户评价
      购物车
        数量增减
        优惠券计算
    管理端
      商品管理
        上架/下架
        库存管理
      订单管理
        发货处理
        退款审核
      数据看板
        销售统计
        用户留存
```

**特点**：
- 使用 `root` 定义中心主题
- 清晰的层级缩进结构
- 覆盖了产品的主要功能模块

---

## 模板2：公司组织架构（评分：92分）⭐⭐⭐⭐

**适用场景**：企业介绍、团队管理、汇报关系

```mermaid
mindmap
  root((科技公司))
    研发中心
      前端组
        Web开发
        移动端开发
      后端组
        Java开发
        Go开发
      测试组
        自动化测试
        性能测试
    产品中心
      产品经理
      UI/UX设计
    市场中心
      品牌推广
      渠道销售
      客户服务
    职能部门
      人力资源
      财务部
      行政部
```

**特点**：
- 展示了典型的部门层级
- 适合展示团队结构

---

## 模板3：全栈技术路线图（评分：94分）⭐⭐⭐⭐⭐

**适用场景**：技术学习、技能树、技术选型

```mermaid
mindmap
  root((全栈开发))
    前端 Frontend
      HTML/CSS
      JavaScript
        ES6+
        TypeScript
      框架
        React
        Vue
        Next.js
    后端 Backend
      语言
        Node.js
        Python
        Go
      数据库
        MySQL
        Redis
        MongoDB
    DevOps
      Docker
      Kubernetes
      CI/CD
        GitHub Actions
        Jenkins
      云服务
        AWS
        Aliyun
```

**特点**：
- 使用混合的中英文标签
- 展示了知识体系的关联性

---

## 模板4：项目会议头脑风暴（评分：88分）⭐⭐⭐⭐

**适用场景**：会议记录、创意发散、问题分析

```mermaid
mindmap
  root((年度营销活动))
    ::icon(fa fa-calendar-check)
    目标 Target
      用户增长 20%
      GMV 突破 500w
    渠道 Channel
      社交媒体
        微信公众号
        抖音/TikTok
      线下活动
        快闪店
        行业展会
    预算 Budget
      广告投放: 50w
      物料制作: 20w
      人员成本: 30w
    风险 Risk
      ::icon(fa fa-exclamation-triangle)
      物流延误
      系统宕机
```

**特点**：
- 使用图标 `::icon()` 增强视觉效果（需支持 FontAwesome 的环境）
- 结构化记录会议要点

---

## 语法参考

### 基本结构
```mermaid
mindmap
  root((中心节点))
    一级节点
      二级节点
      二级节点
    一级节点
      二级节点
```

### 节点形状
Mermaid Mindmap 会根据层级自动分配形状，但也支持部分自定义语法（取决于具体渲染器支持程度），通常通过缩进控制层级即可。

### 图标支持
使用 `::icon(class-name)` 语法添加图标，例如 `::icon(fa fa-book)`。这取决于渲染环境是否加载了图标库（如 FontAwesome）。
