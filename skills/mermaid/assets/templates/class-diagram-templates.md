# Class Diagram 模板库

本文档提供高质量的类图模板，可直接复制使用。

---

## 模板1：简单类关系（评分：85分）⭐⭐⭐⭐

**适用场景**：基础OOP设计、简单继承关系

```mermaid
%%{init: {'theme':'default'}}%%
classDiagram
    class Animal {
        +String name
        +int age
        +eat()
        +sleep()
    }
    
    class Dog {
        +String breed
        +bark()
        +fetch()
    }
    
    class Cat {
        +String color
        +meow()
        +scratch()
    }
    
    Animal <|-- Dog
    Animal <|-- Cat
```

---

## 模板2：电商系统模型（评分：92分）⭐⭐⭐⭐⭐

**适用场景**：电商系统、订单管理、用户模型

```mermaid
%%{init: {'theme':'default'}}%%
classDiagram
    class User {
        +Long id
        +String username
        +String email
        +String password
        +Date createdAt
        +register()
        +login()
        +updateProfile()
    }
    
    class Order {
        +Long id
        +String orderNo
        +OrderStatus status
        +BigDecimal totalAmount
        +Date createdAt
        +create()
        +pay()
        +cancel()
        +complete()
    }
    
    class OrderItem {
        +Long id
        +int quantity
        +BigDecimal price
        +BigDecimal subtotal
        +calculateSubtotal()
    }
    
    class Product {
        +Long id
        +String name
        +String description
        +BigDecimal price
        +int stock
        +updateStock()
        +getDetails()
    }
    
    class Category {
        +Long id
        +String name
        +Long parentId
        +getProducts()
    }
    
    class Address {
        +Long id
        +String province
        +String city
        +String detail
        +String phone
    }
    
    User "1" --> "*" Order : places
    User "1" --> "*" Address : has
    Order "1" *-- "*" OrderItem : contains
    OrderItem "*" --> "1" Product : references
    Product "*" --> "1" Category : belongs to
```

---

## 模板3：设计模式 - 策略模式（评分：88分）⭐⭐⭐⭐

**适用场景**：设计模式、策略模式实现

```mermaid
%%{init: {'theme':'default'}}%%
classDiagram
    class PaymentContext {
        -PaymentStrategy strategy
        +setStrategy(PaymentStrategy)
        +executePayment(amount)
    }
    
    class PaymentStrategy {
        <<interface>>
        +pay(amount)*
        +refund(amount)*
    }
    
    class AlipayStrategy {
        +pay(amount)
        +refund(amount)
    }
    
    class WechatPayStrategy {
        +pay(amount)
        +refund(amount)
    }
    
    class CreditCardStrategy {
        -String cardNumber
        +pay(amount)
        +refund(amount)
        -validateCard()
    }
    
    PaymentContext --> PaymentStrategy
    PaymentStrategy <|.. AlipayStrategy
    PaymentStrategy <|.. WechatPayStrategy
    PaymentStrategy <|.. CreditCardStrategy
```

---

## 模板4：MVC架构（评分：86分）⭐⭐⭐⭐

**适用场景**：MVC模式、Web应用架构

```mermaid
%%{init: {'theme':'default'}}%%
classDiagram
    class Controller {
        <<abstract>>
        #Model model
        #View view
        +handleRequest()
        +updateView()
    }
    
    class UserController {
        +listUsers()
        +createUser()
        +updateUser()
        +deleteUser()
    }
    
    class Model {
        <<abstract>>
        #data
        +getData()
        +setData()
        +validate()
    }
    
    class UserModel {
        -List~User~ users
        +findById()
        +save()
        +delete()
    }
    
    class View {
        <<abstract>>
        +render()
        +update()
    }
    
    class UserListView {
        +render()
        +showError()
    }
    
    Controller <|-- UserController
    Model <|-- UserModel
    View <|-- UserListView
    
    Controller --> Model : uses
    Controller --> View : updates
    View --> Model : observes
```

---

## 模板5：领域驱动设计（评分：90分）⭐⭐⭐⭐⭐

**适用场景**：DDD、领域模型、聚合根

```mermaid
%%{init: {'theme':'default'}}%%
classDiagram
    class Order {
        <<AggregateRoot>>
        +OrderId id
        +CustomerId customerId
        +OrderStatus status
        +List~OrderLine~ lines
        +addLine(product, qty)
        +removeLine(lineId)
        +submit()
        +cancel()
    }
    
    class OrderLine {
        <<Entity>>
        +OrderLineId id
        +ProductId productId
        +int quantity
        +Money unitPrice
        +calculateTotal()
    }
    
    class OrderId {
        <<ValueObject>>
        +String value
        +validate()
    }
    
    class Money {
        <<ValueObject>>
        +BigDecimal amount
        +String currency
        +add(Money)
        +subtract(Money)
    }
    
    class OrderStatus {
        <<Enumeration>>
        DRAFT
        SUBMITTED
        PAID
        SHIPPED
        COMPLETED
        CANCELLED
    }
    
    class OrderRepository {
        <<Repository>>
        +save(Order)
        +findById(OrderId)
        +findByCustomer(CustomerId)
    }
    
    class OrderService {
        <<DomainService>>
        -OrderRepository repository
        +createOrder(customerId)
        +submitOrder(orderId)
    }
    
    Order *-- OrderLine
    Order --> OrderId
    Order --> OrderStatus
    OrderLine --> Money
    OrderRepository --> Order
    OrderService --> OrderRepository
```

---

## 模板6：泛型类（评分：85分）⭐⭐⭐⭐

**适用场景**：泛型设计、容器类

```mermaid
%%{init: {'theme':'default'}}%%
classDiagram
    class Repository~T~ {
        <<interface>>
        +save(T entity)
        +findById(Long id) T
        +findAll() List~T~
        +delete(Long id)
    }
    
    class JpaRepository~T~ {
        -EntityManager em
        +save(T entity)
        +findById(Long id) T
        +findAll() List~T~
        +delete(Long id)
    }
    
    class UserRepository {
        +findByUsername(String) User
        +findByEmail(String) User
    }
    
    class ProductRepository {
        +findByCategory(Long) List~Product~
        +findByPriceRange(min, max) List~Product~
    }
    
    Repository~T~ <|.. JpaRepository~T~
    JpaRepository~T~ <|-- UserRepository
    JpaRepository~T~ <|-- ProductRepository
```

---

## 使用说明

### 关系类型

| 语法 | 说明 | 示例 |
|------|------|------|
| `<\|--` | 继承 | Animal <\|-- Dog |
| `*--` | 组合 | Order *-- OrderItem |
| `o--` | 聚合 | Team o-- Player |
| `-->` | 关联 | User --> Order |
| `--` | 链接 | A -- B |
| `..>` | 依赖 | Controller ..> Service |
| `..\|>` | 实现 | Class ..\|> Interface |

### 可见性修饰符

| 符号 | 含义 |
|------|------|
| `+` | public |
| `-` | private |
| `#` | protected |
| `~` | package |

### 多重性

```mermaid
classDiagram
    A "1" --> "*" B : 一对多
    C "0..1" --> "1..*" D : 零或一对一或多
```

### 注解

```mermaid
classDiagram
    class MyClass {
        <<interface>>
        <<abstract>>
        <<service>>
        <<enumeration>>
    }
```
