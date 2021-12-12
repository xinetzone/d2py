# OOP: The Big Picture

## Why Use Classes? 

程序就是“用一些东西来做事情”，而类就是一种定义新种类的东西的方式，它反映了在程序领域中的真实对象。

类的三个独特性质：

### Multiple instances （多重实例）

类本质上是生成一个或多个对象的工厂。每次调用类时, 都会生成一个具有独特命名空间的新对象。从类生成的每个对象都可以访问类的属性, 并为每个对象的不同数据获取其自己的命名空间。

### Customization via inheritance （通过继承进行定制）

类还支持 OOP 继承概念;我们可以通过在编码为子类的新软件组件中重新定义类本身的属性来扩展类。通常, 类可以建立命名空间层次结构, 定义由层次结构中的类创建的对象所使用的名称。这比其他工具更直接支持多个可自定义的行为。

### Operator overloading（运算符重载）

通过提供特殊的协议方法, 类可以定义响应我们在内置类型的工作中看到的操作类型的对象。例如, 可以对使用类进行的对象进行切片、串联、索引等。Python 提供了类可用于拦截和实现任何内置类型操作的挂钩。

在它的基础上, OOP 在 Python 中的机制主要只是 two bits of magic: 函数中的特殊第一个参数 (接收调用的对象) 和继承属性搜索 (支持通过自定义编程)。除了这一点之外, 模型基本上只是最终处理内置类型的函数。虽然不完全是新的, 但 OOP 添加了额外的结构层, 支持比平面程序模型更好的编程。

*** OOP is as much an experience as a technology.***

## Attribute Inheritance Search （属性继承搜索）

大多数 OOP 均可使用下面的式子来表达：

```python
object.attribute 
```

`class` 产生类时, 表达式在 Python 中启动搜索-它搜索连接对象的树, 查找它可以找到的首次出现的属性。当涉及类时, 前面的 Python 表达式有效地转换为自然语言中的以下内容:

- 通过查找对象, 然后在它上面的所有类中, 从下到上, 从左到右查找属性的第一个匹配项。

换言之, 属性提取只是树搜索。由于树中较低的对象继承附加到该树中较高对象的属性, 因此应用了术语**继承**。当搜索从底部向上进行时, 从某种意义上说, 链接到树中的对象是所有树父级中定义的所有属性的联合, 所有这些特性都达到树的顶端。

我们用代码构建链接对象的树, 而 Python 在每次使用对象时都会在运行时通过 `object.attribute ` 表达式“爬树”去搜索属性。

![](https://img2018.cnblogs.com/blog/685754/201810/685754-20181028221130546-230027578.png)



- Classes 
    - Serve as instance factories. Their attributes provide behavior—data and functions —that is inherited by all the instances generated from them (e.g., a function to compute an employee’s salary from pay and hours).
- Instances 
    - Represent the concrete items in a program’s domain. Their attributes record data that varies per specific object (e.g., an employee’s Social Security number). 

## 类对象提供默认的行为

**类语句创建类对象并为其分配名称**。与函数 `def` 语句一样, Python `class` 语句是可执行语句。运行时, 它将生成一个新的类对象, 并将其分配给类标头中的名称。此外, 与 `def` 一样, 类语句通常在第一次导入它们所编码的文件时运行。

**`class` 语句内的赋值创建类属性**。就像在模块文件中一样, 类语句中的顶层赋值 (不嵌套在 `def` 中) 在类对象中生成属性。从技术上讲, 类语句定义了一个局部作用域, 它会变成类对象的属性命名空间, 就像模块的全局作用域一样。运行类语句后, 将按名称限定: `object.name` 来访问类属性。

**类属性提供对象状态和行为**。类对象的属性记录状态信息和要由类创建的所有实例共享的行为;嵌套在类中的函数 `def` 语句生成处理实例的**方法**。

## Instance Objects Are Concrete Items 

**实例对象是具体的元素**：

- **调用类对象 (如函数) 会产生一个新的实例对象**。每次调用类时, 它都会创建并返回一个新的实例对象。实例表示程序域中的具体项。
- **每个实例对象都继承类属性并获取其自己的命名空间**。从类创建的实例对象是新的命名空间;它们开始为空, 但继承在从中生成它们的类对象中的属性。
- **在方法中对`self` 属性的赋值使每实例属性**。在类的方法函数中, 第一个参数 (一般约定为 `self`) 引用正在处理的实例对象;对自身属性的赋值在实例中创建或更改数据, 而不是类。

最终的结果是类定义公共的、共享的数据和行为, 并生成实例。实例反映具体的应用程序实体, 并记录每个对象可能有所不同的每实例数据。

详细内容见：[类与对象 ](https://www.cnblogs.com/q735613050/p/7351486.html)

## 模块与类的区别

- 模块反映了整个**文件**
- 类只是文件内的**语句**

## 运算符重载


```python
class FirstClass:
    def setdata(self, value):
        self.data = value

    def display(self):
        print('当前的值：', self.data)


class SecondClass(FirstClass):
    def __init__(self, value):
        '''
        构造函数
        '''
        self.data = value

    def __add__(self, other):
        '''
        重载：+
        '''
        return SecondClass(other + self.data)

    def __str__(self):
        '''
        重载：print
        '''
        return '[SecondClass: %s]' % self.data

    def mul(self, other):
        self.data *= other
```


```python
a = SecondClass('abc')
a.display()
```

    当前的值： abc
    


```python
print(a)
```

    [SecondClass: abc]
    


```python
b = a + 'xyz'

print(b)
```

    [SecondClass: xyzabc]
    


```python
a.mul(3)

print(a)
```

    [SecondClass: abcabcabc]
    

## 类与字典


```python
class rec:
    pass
```

为 `rec` 类添加属性：


```python
rec.name = 'Bob'
rec.age = 40
```


```python
print(rec.name)
```

    Bob
    


```python
x = rec()
y = rec()
```


```python
x.name, y.name
```




    ('Bob', 'Bob')




```python
x.name = 'Sue'
rec.name, x.name, y.name
```




    ('Bob', 'Sue', 'Bob')



命名空间对象的属性通常都是以字典的形式实现的，而类继承树（一般而言）只是连接至其他字典的字典而已。例如， `__dict__` 属性是针对大多数基于类的对象的命名空间字典 （一些类也可能在 `__slots__` 中定义属性）。


```python
rec.__dict__.keys()
```




    dict_keys(['__module__', '__dict__', '__weakref__', '__doc__', 'name', 'age'])




```python
list(x.__dict__.keys())
```




    ['name']




```python
list(y.__dict__.keys())
```




    []



使用 `__class__` 获取实例的继承：


```python
x.__class__
```




    __main__.rec



使用 `__bases__` 获取类的超类：


```python
rec.__bases__
```




    (object,)



Python 的类模型是相当动态：类和实例只是命名空间对象，属性是通过赋值语句动态建立的。

类中的函数 （`def` 语句）一般称作**方法**，代表类的逻辑。