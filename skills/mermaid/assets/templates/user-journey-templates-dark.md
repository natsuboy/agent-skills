# User Journey Dark 模板库

本文档提供适用于深色背景编辑器的 Mermaid User Journey Diagram 模板。

**适用场景**：
- Dark 模式编辑器
- 深色背景演示文稿

---

## 模板1：电商购物旅程 (Dark)（评分：95分）⭐⭐⭐⭐⭐

```mermaid
%%{init: {'theme': 'dark'}}%%
journey
    title 用户在电商网站的购物旅程
    section 浏览与发现
      浏览首页: 5: 用户
      搜索商品: 4: 用户
      查看商品详情: 5: 用户
    section 决策与购买
      加入购物车: 5: 用户
      查看购物车: 4: 用户
      结算支付: 3: 用户, 支付系统
    section 售后服务
      查看订单状态: 5: 用户
      收到商品: 5: 用户
      评价商品: 4: 用户
```

---

## 模板2：新用户注册引导 (Dark)（评分：92分）⭐⭐⭐⭐

```mermaid
%%{init: {'theme': 'dark'}}%%
journey
    title 新用户注册与引导流程
    section 注册阶段
      访问落地页: 5: 访客
      点击注册: 5: 访客
      填写表单: 3: 访客
      接收验证码: 4: 系统
      验证通过: 5: 系统
    section 引导阶段
      欢迎页面: 5: 新用户
      功能演示: 4: 新用户
      设置偏好: 3: 新用户
      完成引导: 5: 新用户
    section 首次使用
      创建第一个项目: 4: 新用户
      邀请成员: 4: 新用户
```

---

## 模板3：客户服务工单流程 (Dark)（评分：90分）⭐⭐⭐⭐

```mermaid
%%{init: {'theme': 'dark'}}%%
journey
    title 客户支持工单处理流程
    section 提交问题
      发现问题: 2: 客户
      查找帮助文档: 3: 客户
      提交工单: 4: 客户
    section 处理中
      系统自动回复: 5: 机器人
      客服接单: 4: 客服专员
      沟通细节: 3: 客户, 客服专员
      定位问题: 4: 技术支持
    section 问题解决
      提供解决方案: 5: 客服专员
      验证修复: 4: 客户
      关闭工单: 5: 客户
      满意度调查: 5: 客户
```

---

## 模板4：移动应用登录与安全 (Dark)（评分：88分）⭐⭐⭐⭐

```mermaid
%%{init: {'theme': 'dark'}}%%
journey
    title 移动应用安全登录流程
    section 启动
      打开App: 5: 用户
      自动登录检测: 5: App
    section 认证
      输入密码: 3: 用户
      FaceID验证: 5: 用户, 系统
      两步验证(2FA): 3: 用户, 短信服务
    section 授权
      获取Token: 5: 服务器
      加载主页: 5: App
      同步数据: 4: App, 服务器
```

---

## 视觉配置
User Journey 图表在 Dark 模式下的颜色配置通常由 `theme: dark` 自动处理，但你可以通过 `themeVariables` 微调：

```mermaid
%%{init: {
  'theme': 'dark',
  'themeVariables': {
    'actorBkg': '#1f2937',
    'actorBorder': '#60a5fa',
    'signalColor': '#d1d5db',
    'signalTextColor': '#f3f4f6'
  }
}}%%
journey
    title 自定义颜色的旅程图
    section 示例
      任务A: 5: 用户
      任务B: 3: 用户
```
