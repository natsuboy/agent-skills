# Pie Chart Dark 模板库

本文档提供适用于深色背景编辑器的 Mermaid Pie Chart 模板。

**适用场景**：
- Dark 模式编辑器
- 深色背景仪表板

---

## 模板1：市场份额分布 (Dark)（评分：95分）⭐⭐⭐⭐⭐

```mermaid
%%{init: {'theme': 'dark'}}%%
pie title 2024年全球云服务市场份额
    "AWS" : 32
    "Azure" : 23
    "Google Cloud" : 10
    "Alibaba Cloud" : 6
    "IBM Cloud" : 4
    "其他" : 25
```

---

## 模板2：项目预算分配 (Dark)（评分：92分）⭐⭐⭐⭐

```mermaid
%%{init: {'theme': 'dark'}}%%
pie showData
    title 年度IT预算分配 (单位: 万美元)
    "研发与开发" : 450
    "基础设施" : 200
    "软件许可" : 150
    "运维支持" : 120
    "安全合规" : 80
```

---

## 模板3：用户满意度调查 (Dark)（评分：90分）⭐⭐⭐⭐

```mermaid
%%{init: {'theme': 'dark'}}%%
pie title 产品满意度调查结果
    "非常满意" : 42
    "满意" : 35
    "一般" : 15
    "不满意" : 5
    "非常不满意" : 3
```

---

## 模板4：代码库语言构成 (Dark)（评分：88分）⭐⭐⭐⭐

```mermaid
%%{init: {'theme': 'dark'}}%%
pie showData
    title 项目代码行数构成
    "TypeScript" : 68.5
    "Python" : 15.2
    "HTML/CSS" : 10.1
    "Shell" : 4.2
    "Dockerfile" : 2.0
```

---

## 视觉配置 (Dark Mode)

在 Dark 模式下，默认配色通常已经足够清晰。如果需要自定义切片颜色，可以使用 `themeVariables`：

```mermaid
%%{init: {
  'theme': 'dark',
  'themeVariables': {
    'pie1': '#3b82f6',
    'pie2': '#10b981',
    'pie3': '#f59e0b',
    'pie4': '#ef4444',
    'pie5': '#8b5cf6',
    'pie6': '#6b7280'
  }
}}%%
pie title 自定义颜色的饼图
    "类别A" : 40
    "类别B" : 30
    "类别C" : 20
    "类别D" : 10
```
