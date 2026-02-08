# Gantt 模板库

本文档提供高质量的甘特图模板，可直接复制使用。

---

## 模板1：简单项目计划（评分：85分）⭐⭐⭐⭐

**适用场景**：简单项目、短期计划

```mermaid
%%{init: {'theme':'default'}}%%
gantt
    title 项目开发计划
    dateFormat YYYY-MM-DD
    
    section 阶段1
    任务1 :a1, 2026-01-01, 7d
    任务2 :a2, after a1, 5d
    
    section 阶段2
    任务3 :b1, after a2, 7d
    任务4 :b2, after b1, 3d
```

---

## 模板2：软件开发项目（评分：92分）⭐⭐⭐⭐⭐

**适用场景**：软件开发、敏捷项目、迭代计划

```mermaid
%%{init: {'theme':'default'}}%%
gantt
    title 电商系统开发计划
    dateFormat YYYY-MM-DD
    excludes weekends
    
    section 📋 需求阶段
    需求调研         :done, req1, 2026-01-06, 5d
    需求分析         :done, req2, after req1, 3d
    需求评审         :done, req3, after req2, 2d
    
    section 🎨 设计阶段
    系统架构设计     :done, des1, after req3, 4d
    数据库设计       :done, des2, after des1, 3d
    API接口设计      :active, des3, after des1, 4d
    UI/UX设计        :active, des4, after req3, 8d
    
    section 💻 开发阶段
    后端开发-用户模块 :dev1, after des2, 10d
    后端开发-订单模块 :dev2, after dev1, 8d
    后端开发-支付模块 :dev3, after dev2, 6d
    前端开发         :dev4, after des4, 15d
    接口联调         :dev5, after dev3, 5d
    
    section 🧪 测试阶段
    单元测试         :test1, after dev1, 15d
    集成测试         :crit, test2, after dev5, 7d
    性能测试         :test3, after test2, 4d
    用户验收测试     :test4, after test3, 5d
    
    section 🚀 上线阶段
    部署准备         :rel1, after test4, 2d
    生产部署         :crit, rel2, after rel1, 1d
    监控观察         :rel3, after rel2, 5d
    
    section 📌 里程碑
    需求冻结         :milestone, m1, after req3, 0d
    开发完成         :milestone, m2, after dev5, 0d
    正式上线         :milestone, m3, after rel2, 0d
```

---

## 模板3：产品发布计划（评分：88分）⭐⭐⭐⭐

**适用场景**：产品发布、市场活动

```mermaid
%%{init: {'theme':'default'}}%%
gantt
    title 产品发布计划 v2.0
    dateFormat YYYY-MM-DD
    
    section 产品准备
    功能开发完成     :done, p1, 2026-02-01, 2026-02-28
    文档编写         :active, p2, 2026-02-15, 15d
    Demo准备         :p3, after p2, 5d
    
    section 市场准备
    发布材料准备     :m1, 2026-02-20, 10d
    媒体联络         :m2, after m1, 7d
    预热活动         :m3, after m2, 5d
    
    section 销售准备
    销售培训         :s1, 2026-02-25, 5d
    客户预约         :s2, after s1, 10d
    
    section 发布活动
    发布会           :crit, r1, 2026-03-20, 1d
    媒体报道         :r2, after r1, 7d
    客户跟进         :r3, after r1, 14d
```

---

## 模板4：Sprint计划（评分：86分）⭐⭐⭐⭐

**适用场景**：敏捷开发、Sprint规划

```mermaid
%%{init: {'theme':'default'}}%%
gantt
    title Sprint 10 计划
    dateFormat YYYY-MM-DD
    
    section 用户故事1
    US-101 登录优化   :crit, us101, 2026-03-01, 3d
    US-102 密码重置   :us102, after us101, 2d
    
    section 用户故事2
    US-103 购物车改版 :us103, 2026-03-01, 4d
    US-104 结算流程   :crit, us104, after us103, 3d
    
    section 用户故事3
    US-105 订单列表   :us105, 2026-03-03, 3d
    US-106 订单详情   :us106, after us105, 2d
    
    section 技术任务
    代码重构         :tech1, 2026-03-01, 5d
    性能优化         :tech2, after tech1, 3d
    
    section Sprint活动
    Sprint规划       :milestone, sp1, 2026-03-01, 0d
    每日站会         :daily, 2026-03-01, 14d
    Sprint评审       :milestone, sp2, 2026-03-14, 0d
```

---

## 模板5：多团队协作（评分：87分）⭐⭐⭐⭐

**适用场景**：多团队项目、跨部门协作

```mermaid
%%{init: {'theme':'default'}}%%
gantt
    title 多团队协作项目
    dateFormat YYYY-MM-DD
    
    section 后端团队
    API开发          :be1, 2026-01-01, 20d
    数据库优化       :be2, after be1, 10d
    缓存集成         :be3, after be2, 5d
    
    section 前端团队
    UI组件开发       :fe1, 2026-01-01, 15d
    页面开发         :fe2, after fe1, 12d
    联调优化         :fe3, after be1, 8d
    
    section 移动团队
    iOS开发          :mob1, 2026-01-08, 25d
    Android开发      :mob2, 2026-01-08, 25d
    移动端联调       :mob3, after be1, 10d
    
    section QA团队
    测试用例编写     :qa1, 2026-01-01, 10d
    接口测试         :qa2, after be1, 8d
    端到端测试       :qa3, after fe3, 7d
    
    section 运维团队
    环境准备         :ops1, 2026-01-15, 5d
    部署脚本         :ops2, after ops1, 5d
    上线部署         :crit, ops3, after qa3, 2d
```

---

## 使用说明

### 基本语法

```mermaid
gantt
    title 图表标题
    dateFormat YYYY-MM-DD
    
    section 阶段名称
    任务名称 :状态, id, 开始日期, 结束日期或持续时间
```

### 日期格式

| 格式 | 示例 |
|------|------|
| `YYYY-MM-DD` | 2026-01-15 |
| `DD-MM-YYYY` | 15-01-2026 |
| `YYYY-MM-DD HH:mm` | 2026-01-15 10:00 |

### 任务定义方式

```mermaid
gantt
    %% 固定日期范围
    任务1 :a1, 2026-01-01, 2026-01-10
    
    %% 开始日期 + 持续时间
    任务2 :a2, 2026-01-01, 10d
    
    %% 依赖前置任务
    任务3 :a3, after a1, 5d
    
    %% 多个前置依赖
    任务4 :a4, after a1 a2, 5d
```

### 任务状态

| 状态 | 说明 | 显示效果 |
|------|------|----------|
| `done` | 已完成 | 灰色填充 |
| `active` | 进行中 | 蓝色边框 |
| `crit` | 关键任务 | 红色填充 |
| (无) | 待开始 | 默认样式 |

### 里程碑

```mermaid
gantt
    里程碑名称 :milestone, m1, 2026-01-15, 0d
```

### 排除日期

```mermaid
gantt
    excludes weekends                    %% 排除周末
    excludes 2026-01-01, 2026-05-01     %% 排除特定日期
```

### 时间轴模式

```mermaid
gantt
    %% 周显示模式
    tickInterval 1week
    
    %% 月显示模式
    tickInterval 1month
```
