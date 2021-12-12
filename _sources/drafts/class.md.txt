# class 

## [Python 作用域和命名空间](http://www.pythondoc.com/pythontutorial3/classes.html#id27)
类的定义非常巧妙的运用了命名空间，要完全理解接下来的知识，需要先理解作用域和命名空间的工作原理。另外，这一切的知识对于任何高级 Python 程序员都非常有用。

**命名空间** 是从命名到对象的映射。       
当前命名空间主要是通过 Python 字典实现的，不过通常不关心具体的实现方式（除非出于性能考虑），以后也有可能会改变其实现方式。

以下有一些命名空间的例子：内置命名（像 abs() 这样的函数，以及内置异常名）集，模块中的全局命名，函数调用中的局部命名。某种意义上讲对象的属性集也是一个命名空间。关于命名空间需要了解的一件很重要的事就是不同命名空间中的命名没有任何联系，例如两个不同的模块可能都会定义一个名为 maximize 的函数而不会发生混淆－用户必须以模块名为前缀来引用它们。

称 Python 中任何一个“`.`”之后的命名为 **属性**      
例如，表达式 `z.real` 中的 `real` 是对象 `z` 的一个属性。     
严格来讲，从模块中引用命名是引用属性：      
表达式 `modname.funcname` 中，`modname` 是一个模块对象，`funcname` 是它的一个属性。          
因此，模块的属性和模块中的全局命名有直接的映射关系：它们共享同一命名空间！

属性可以是只读过或写的。后一种情况下，可以对属性赋值。你可以这样： `modname.the_answer = 42 `。可写的属性也可以用 `del 语句`删除。   
例如： `del modname.the_answer` 会从 `modname 对象`中删除 `the_answer 属性`。

不同的命名空间在不同的时刻创建，有不同的生存期。包含内置命名的命名空间在 Python 解释器启动时创建，会一直保留，不被删除。模块的全局命名空间在模块定义被读入时创建，通常，模块命名空间也会一直保存到解释器退出。由解释器在最高层调用执行的语句，不管它是从脚本文件中读入还是来自交互式输入，都是 `__main__` 模块的一部分，所以它们也拥有自己的命名空间（内置命名也同样被包含在一个模块中，它被称作 `builtins` ）。

当调用函数时，就会为它创建一个`局部命名空间`，并且在函数返回或抛出一个并没有在函数内部处理的异常时被删除。（实际上，用遗忘来形容到底发生了什么更为贴切。）当然，每个递归调用都有自己的局部命名空间。

`作用域` 就是一个 Python 程序可以直接访问命名空间的正文区域。这里的直接访问意思是一个对名称的错误引用会尝试在命名空间内查找。尽管作用域是静态定义，在使用时他们都是动态的。每次执行时，至少有三个命名空间可以直接访问的作用域嵌套在一起：
   - 包含局部命名的使用域在最里面，首先被搜索；其次搜索的是中层的作用域，这里包含了同级的函数；
   - 最后搜索最外面的作用域，它包含内置命名。
- 首先搜索最内层的作用域，它包含局部命名任意函数包含的作用域，是内层嵌套作用域搜索起点，包含非局部，但是也非全局的命名
- 接下来的作用域包含当前模块的全局命名
- 最外层的作用域（最后搜索）是包含内置命名的命名空间

以下是一个示例，演示了如何引用不同作用域和命名空间，以及 global 和 nonlocal 如何影响变量绑定:


```python
def scope_test():
    def do_local():
        spam = "local spam"
    def do_nonlocal():
        nonlocal spam
        spam = "nonlocal spam"
    def do_global():
        global spam
        spam = "global spam"
    spam = "test spam"
    do_local()
    print("After local assignment:", spam)
    do_nonlocal()
    print("After nonlocal assignment:", spam)
    do_global()
    print("After global assignment:", spam)

scope_test()
print("In global scope:", spam)
```

    After local assignment: test spam
    After nonlocal assignment: nonlocal spam
    After global assignment: nonlocal spam
    In global scope: global spam
    

local 赋值语句是无法改变 scope_test 的 spam 绑定。nonlocal 赋值语句改变了 scope_test 的 spam 绑定，并且 global 赋值语句从模块级改变了 spam 绑定。

# 类

|名词|描述|
|:-|:-|
|类(Class)|用来描述具有相同的属性和方法的对象的集合。它定义了该集合中每个对象所共有的属性和方法。对象是类的实例。|
|类变量|类变量在整个实例化的对象中是公用的。类变量定义在类中且在函数体之外。类变量通常不作为实例变量使用。|
|数据成员|类变量或者实例变量用于处理类及其实例对象的相关的数据。|
|方法重写|如果从父类继承的方法不能满足子类的需求，可以对其进行改写，这个过程叫方法的覆盖（override），也称为方法的重写。|
|实例变量|定义在方法中的变量，只作用于当前实例的类。|
|继承|即一个派生类（derived class）继承基类（base class）的字段和方法。继承也允许把一个派生类的对象作为一个基类对象对待。例如，有这样一个设计：一个Dog类型的对象派生自Animal类，这是模拟"是一个（is-a）"关系（例图，Dog是一个Animal）。|
|实例化|创建一个类的实例，类的具体对象。|
|方法|类中定义的函数。|
|对象|通过类定义的数据结构实例。对象包括两个数据成员（类变量和实例变量）和方法(实例方法，类方法，静态方法)|

# 空行
函数之间或类的方法之间用空行分隔，表示一段新的代码的开始。类和函数入口之间也用一行空行分隔，以突出函数入口的开始。
空行与代码缩进不同，空行并不是Python语法的一部分。书写时不插入空行，Python解释器运行也不会出错。但是空行的作用在于分隔两段不同功能或含义的代码，便于日后代码的维护或重构。

记住：空行也是程序代码的一部分。

```
和其它编程语言相比，Python 在尽可能不增加新的语法和语义的情况下加入了类机制。
Python中的类提供了面向对象编程的所有基本功能：类的继承机制允许多个基类，派生类可以覆盖基类中的任何方法，方法中可以调用基类中的同名方法。 
对象可以包含任意数量和类型的数据。
```

# 类的格式：
```python 
class ClassName(SuperClass1,SuperClass2,...):
    '''
    optional documentation string
    '''
    Class_suite
```

## 一些说明
- 数据属性会覆盖同名的方法属性。为了避免意外的名称冲突，这在大型程序中是极难发现的 Bug，使用一些约定来减少冲突的机会是明智的。
    + 可能的约定包括：大写方法名称的首字母，使用一个唯一的小字符串（也许只是一个下划线）作为数据属性名称的前缀，或者方法使用动词而数据属性使用名词。
- 数据属性可以被方法引用，也可以由一个对象的普通用户（客户）使用。换句话说，类不能用来实现纯净的数据类型。    
    事实上，Python 中不可能强制隐藏数据——一切基于约定（如果需要，使用 C 编写的 Python 实现可以完全隐藏实现细节并控制对象的访问。这可以用来通过 C 语言扩展 Python）。
- 客户应该谨慎的使用数据属性——客户可能通过践踏他们的数据属性而使那些由方法维护的常量变得混乱。   
    注意：只要能避免冲突，客户可以向一个实例对象添加他们自己的数据属性，而不会影响方法的正确性——再次强调，命名约定可以避免很多麻烦。
- 从方法内部引用数据属性（或其他方法）并没有快捷方式。这实际上增加了方法的可读性：当浏览一个方法时，在局部变量和实例变量之间不会出现令人费解的情况。
- 一般，方法的第一个参数被命名为 self。   
    这仅仅是一个约定：对 Python 而言，名称 `self` 绝对没有任何特殊含义。（但是请注意：如果不遵循这个约定，对其他的 Python 程序员而言你的代码可读性就会变差，而且有些 类查看器 程序也可能是遵循此约定编写的。）
- 类属性的任何函数对象都为那个类的实例定义了一个方法。函数定义代码不一定非得定义在类中：也可以将一个函数对象赋值给类中的一个局部变量。   
例如:


```python
# Function defined outside the class
def f1(self, x, y):
    return min(x, x+y)

class C(object):
    f = f1
    def g(self):
        return 'hello world'
    h = g
```

```
现在 f,g和h都是类C的属性，引用的都是函数对象，因此它们都是 C 实例的方法－－ h 严格等于g。
通过 self 参数的方法属性，方法可以调用其它的方法:
```

**类**可以看作是一种把对象分组归类的方法。

# 旧式类的定义(即将被淘汰)

新式类与旧式类的区别主要表现在对超类命名空间检索的使用算法不同。

旧式类可以直接省略括号和超类列表，而新式类以object作为Python中所有类的默认超类。


```python
# 定义Ball1球类
class Ball1:
    def bounce(self):     # self可以看作是类本身的一个实例的引用。
        if self.direction=='down':
            self.direction='up'
            
# 创建一个Ball1球类的实例myBall1
myBall1=Ball1()
```


```python
# 定义myBall1的属性方法之一
myBall1.direction='down'
myBall1.color='red'
myBall1.size='small'
```


```python
# 调用bounce()方法
myBall1.bounce()
```


```python
# 定义属性的方法之二：初始化对象
class Ball2:
    def __init__(self,color,size,direction):
        self.color=color
        self.size=size
        self.direction=direction
        
    def bounce(self):
        if self.direction=='down':
            self.direction='up'
            
myBall2=Ball2('red','small','down')
myBall2.bounce()
```


```python
class Ball3:
    def __init__(self,color,size,direction):
        self.color=color
        self.size=size
        self.direction=direction
        
    def __str__(self):
        msg='Hi,I\'m a '+self.size+' '+self.color+' '+'ball!'
        return msg
    
myBall=Ball3('red','small','down')
print(myBall)
```

    Hi,I'm a small red ball!
    


```python
# 修改属性
myBall.color='black'
myBall.color
```




    'black'




```python
myBall=Ball3('red','big','down')
myBall.size
```




    'big'




```python
print(myBall)
```

    Hi,I'm a big red ball!
    

## 类对象
类对象支持两种操作：属性引用和实例化。
- 属性引用使用和 Python 中所有的属性引用一样的标准语法：`obj.name`。
- 类对象创建后，类命名空间中所有的命名都是有效属性名。

示例：

类实例化后，可以使用其属性，实际上，创建一个类之后，可以通过类名访问其属性。


```python
class MyClass:
    """一个简单的类实例"""
    i = 12345
    def f(self):
        return 'hello world'

# 实例化类
x = MyClass()
 
# 访问类的属性和方法
print("MyClass 类的属性 i 为：", x.i)
print("MyClass 类的方法 f 输出为：", x.f())
```

    MyClass 类的属性 i 为： 12345
    MyClass 类的方法 f 输出为： hello world
    

很多类都倾向于将对象创建为有初始状态的。因此类可能会定义一个名为 `__init__()` 的特殊方法（构造方法），像下面这样：


```python
def __init__(self):
    self.data = []
```

类定义了 `__init__()` 方法的话，类的实例化操作会自动调用 `__init__()` 方法。所以在下例中，可以这样创建一个新的实例:


```python
x = MyClass()
```

当然，`__init__()` 方法可以有参数，参数通过 `__init__()` 传递到类的实例化操作上。例如: 


```python
class Complex:
    def __init__(self, realpart, imagpart):
        self.r = realpart
        self.i = imagpart
x = Complex(3.0, -4.5)
print(x.r, x.i)  
```

    3.0 -4.5
    

## 类的方法
在类地内部，使用 `def` 关键字来定义一个方法，与一般函数定义不同，类方法必须包含参数 self, 且为第一个参数，self 代表的是类的实例。 

### **self代表类的实例，而非类**         
类的方法与普通的函数只有一个特别的区别——它们必须有一个额外的第一个参数名称, 按照惯例它的名称是self。


```python
class Test:
    def prt(self):
        print(self)
        print(self.__class__)

t = Test()
t.prt()
```

    <__main__.Test object at 0x0000015BDD989630>
    <class '__main__.Test'>
    

从执行结果可以很明显的看出，self 代表的是类的实例，代表当前对象的地址，而 self.class 则指向类。     
self 不是 python 关键字，我们把他换成 runoob 也是可以正常执行的:


```python
class Test:
    def prt(runoob):
        print(runoob)
        print(runoob.__class__)

t = Test()
t.prt()
```

    <__main__.Test object at 0x000001BD61AB2668>
    <class '__main__.Test'>
    


```python
#类定义
class people:
    #定义基本属性
    name = ''
    age = 0
    #定义私有属性,私有属性在类外部无法直接进行访问
    __weight = 0
    #定义构造方法
    def __init__(self,n,a,w):
        self.name = n
        self.age = a
        self.__weight = w
    def speak(self):
        print("%s 说: 我 %d 岁。" %(self.name,self.age))

# 实例化类
p = people('runoob',10,30)
p.speak()
```

    runoob 说: 我 10 岁。
    


```python
type(p)
```




    __main__.people



 # 新式类

类的成员：         
- 成员变量：       
    - 实例变量
    - 类变量
- 成员方法：       
    - 实例方法
    - 类方法
    - 静态方法
- property(修饰器)

## 创建实例


```python
class Bird(object):    # object类是Python中所有类的默认超类。
    pass       # pass不做任何事情，一般用做占位语句，以保持程序结构的完整性。
```


```python
# b1,b2,b3均是绑定了Bird类实例对象的引用。
b1=Bird()
b2=Bird()
b3=Bird()
a=[b1,b2,b3]
type(a[0])
```




    __main__.Bird



## 实例成员方法 & 实例变量


```python
# 实例方法：setCoordinate，getCoordinate，move,pr
# 实例成员变量(属性变量)：self(对类的实例自身的引用)，x，y
class Bird(object):
    def setCoordinate(self,x,y):   
        self.x,self.y=x,y
    def getCoordinate(self):
        print(self.x,self.y)
    def move(self,dx,dy):
        self.x += dx
        self.y += dy
       
    def pr(self):
        print(self)
        print(self.__class__)
        print(self.x.__class__)
        print(self.getCoordinate().__class__)
```


```python
# 创建实例
bird=Bird()
# 调用实例方法
bird.setCoordinate(1,1)
bird.getCoordinate()
```

    1 1
    


```python
bird.pr()
```

    <__main__.Bird object at 0x000001BD6197C5F8>
    <class '__main__.Bird'>
    <class 'int'>
    1 1
    <class 'NoneType'>
    


```python
bird.move(1,2)
bird.getCoordinate()
```

    2 3
    

### 直接访问实例变量


```python
bird.x
```




    2




```python
bird.x,bird.y=3,3
print(bird.x,bird.y)
```

    3 3
    


```python
bird.x+=2
bird.y+=1
bird.x,bird.y
```




    (5, 4)



## 在对象的属性或方法前加上双下划线(__)可使之变为**私有**
以下均以例子说明：

### 私有成员变量


```python
class Bird(object):
    def setCoordinate(self,x,y):   
        self.__x,self.__y=x,y
    def getCoordinate(self):
        print(self.__x,self.__y)
```


```python
bird=Bird()
bird.setCoordinate(1,1)
bird.getCoordinate()
```

    1 1
    


```python
bird.__x   # 在类外直接访问私有变量，python解释器会抛出一个异常。
```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-102-373560fcf103> in <module>()
    ----> 1 bird.__x   # 在类外直接访问私有变量，python解释器会抛出一个异常。
    

    AttributeError: 'Bird' object has no attribute '__x'


---
**Python的私有并不是绝对的。**           
Python解释器对于类中所有加了双下划线的成员名会做一些名字上的替换，若存在一个成员的名字为`__fooName`,则解释器会在检测到它存在后将其替换为`_ClassName__fooName`,即在成员名前加上单下划线开头的类名。    



```python
bird._Bird__x
```




    1



---

### 类属性与方法的所有
- 类的私有属性     
    `__private_attrs`：两个下划线开头，声明该属性为私有，不能在类地外部被使用或直接访问。在类内部的方法中使用时 `self.__private_attrs`。
- 类的方法       
    在类地内部，使用 def 关键字来定义一个方法，与一般函数定义不同，类方法必须包含参数 self，且为第一个参数，self 代表的是类的实例。
    self 的名字并不是规定死的，也可以使用 this，但是最好还是按照约定是用 self。
- 类的私有方法    
`__private_method`：两个下划线开头，声明该方法为私有方法，只能在类的内部调用 ，不能在类地外部调用。`self.__private_methods`。 


```python
class JustCounter(object):
    __secretCount = 0  # 私有变量
    publicCount = 0    # 公开变量
 
    def count(self):
        self.__secretCount += 1
        self.publicCount += 1
        print (self.__secretCount)

counter = JustCounter()
counter.count()
counter.count()
print (counter.publicCount)
print (counter.__secretCount)  # 报错，实例不能访问私有变量
```

    1
    2
    2
    


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-104-9a9ab8650dbe> in <module>()
         12 counter.count()
         13 print (counter.publicCount)
    ---> 14 print (counter.__secretCount)  # 报错，实例不能访问私有变量
    

    AttributeError: 'JustCounter' object has no attribute '__secretCount'



```python
class Site(object):
    def __init__(self, name, url):
        self.name = name       # public
        self.__url = url   # private
 
    def who(self):
        print('name  : ', self.name)
        print('url : ', self.__url)
 
    def __foo(self):          # 私有方法
        print('这是私有方法')
 
    def foo(self):            # 公共方法
        print('这是公共方法')
        self.__foo()

x = Site('菜鸟教程', 'www.runoob.com')
x.who()        # 正常输出
x.foo()        # 正常输出
x.__foo()      # 报错
```

    name  :  菜鸟教程
    url :  www.runoob.com
    这是公共方法
    这是私有方法
    


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-105-211d0443cb75> in <module>()
         18 x.who()        # 正常输出
         19 x.foo()        # 正常输出
    ---> 20 x.__foo()      # 报错
    

    AttributeError: 'Site' object has no attribute '__foo'


类的专有方法：
- `__init__` : 构造函数，在生成对象时调用
- `__del__ `: 析构函数，释放对象时使用
- `__repr__` : 打印，转换
- `__setitem__ `: 按照索引赋值
- `__getitem__`: 按照索引获取值
- `__len__`: 获得长度
- `__cmp__`: 比较运算
- `__call__`: 函数调用
- `__add__`: 加运算
- `__sub__`: 减运算
- `__mul__`: 乘运算
- `__div__`: 除运算
- `__mod__`: 求余运算
- `__pow__`: 乘方

## 类变量 & 类方法


```python
# 实现一个Bird类，包括两个类成员变量(name_zh,name_en)和两个类成员方法(getName,setName):
class Bird(object):
    name_zh=u'鸟类'
    name_en=u'bird'
    
    @classmethod
    def getName(cls,type):
        if type=='zh':
            return cls.name_zh
        else:
            return cls.name_en
        
    @classmethod
    def setName(cls,type,new_name):
        if type=='zh':
            cls.name_zh=new_name
        else:
            cls.name_en=new_name
```


```python
# 调用和访问类方法和类变量
Bird.getName('zh')
```




    '鸟类'




```python
Bird.name_en
```




    'bird'




```python
Bird.setName('en','birdbird')
Bird.getName('en')
```




    'birdbird'




```python
Bird.name_zh='新鸟类'
Bird.name_zh
```




    '新鸟类'



类变量和类方法可以被实例成员方法以只读的方式访问。


```python
class Bird(object):
    name=u'bird'
    @classmethod
    def getName(cls):
        return cls.name
    def getName2(self):
        print('directly:',self.name)
        print('by call classmethod:',self.getName())
```


```python
bird=Bird()
bird.getName2()
```

    directly: bird
    by call classmethod: bird
    


```python
bird.name
```




    'bird'




```python
bird.getName()
```




    'bird'



### 一个小'bug'


```python
class Bird(object):
    name=u'bird'
    def setName(self,new_name):
        self.name=new_name
```


```python
bird=Bird()
```


```python
bird.name
```




    'bird'




```python
Bird.name
```




    'bird'




```python
bird.setName('birdbird')    # 非读操作，且bird命名空间中没有name变量，故需要创建一个叫name的实例变量。
bird.name
```




    'birdbird'




```python
Bird.name  #Bird访问的依然是类变量的值。
```




    'bird'



## 静态方法
静态方法位于类命名空间中的一种特殊函数，无法对任何实例成员进行操作。

### 实现封装


```python
class Math(object):
    @staticmethod
    def pow(x,y):
        pass
    @staticmethod
    def sqrt(x):
        pass
    @staticmethod
    def log(x):
        pass
```

### 调用

可以访问类变量和类方法，但是，类的实例对象无法调用静态方法。


```python
class Bird(object):
    name=u'bird'
    @staticmethod
    def setName(new_name):
        Bird.name=new_name
```


```python
Bird.name
```




    'bird'




```python
Bird.setName('birdbird')
Bird.name
```




    'birdbird'



## property 修饰器

目的：      
    修饰实例方法，以改变对外的访问方式，使得其在外部被访问时更像是在访问一个变量，而非函数。


```python
class Bird(object):
    def __init__(self,name):
        self.__name=name
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self,name):
        self.__name=name
    @name.deleter
    def name(self):
        del self.__name
```


```python
bird=Bird('bird')
```


```python
bird.name
```




    'bird'




```python
bird.name='birdbird'
bird.name
```




    'birdbird'




```python
del bird.name
```


```python
bird.name
```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-136-3d2d6764ec0c> in <module>()
    ----> 1 bird.name
    

    <ipython-input-131-7072a73d10cd> in name(self)
          4     @property
          5     def name(self):
    ----> 6         return self.__name
          7     @name.setter
          8     def name(self,name):
    

    AttributeError: 'Bird' object has no attribute '_Bird__name'

从上述结果可以看出，Bird类的名叫`name`的对象完全成为了`__name`的替身。有了`name`作为访问的中间层，一些验证的逻辑就可以在`name`的方法中实现了。

## 类的初始化

`__init__`关键字是类的构造方法。           
在Python中，为一个类创建一个 实例对象 时，会立即调用类的构造方法（即当对象被创建后，Python解释器会去类中查找`__init__`函数）。      

`__init__`函数为类添加一些初始化的属性或功能。
```python
class Bird(object):
    def __init__(self,name=None):
        if name:
            self.name=name
```


```python
class Bird(object):
    def __init__(self,*args,**kwargs):
        if kwargs.get('name',None):
            self.name=kwargs['name']
        if kwargs.get('weight',None):
            self.weight=kwargs['weight']
```


```python
bird_1=Bird(name='bird_1',weight=1)
```


```python
bird_1.name
```




    'bird_1'




```python
bird_1.weight
```




    1



# 继承
类的继承：     
- 函数重写 
- 多重继承


Python 同样支持类的继承，如果一种语言不支持继承，类就没有什么意义。派生类的定义如下所示:
```
class DerivedClassName(BaseClassName1):
    <statement-1>
    .
    .
    .
    <statement-N>
```
## 多重继承
需要注意圆括号中基类的顺序，若是基类中有相同的方法名，而在子类使用时未指定，python从左至右搜索 即方法在子类中未找到时，从左到右查找基类中是否包含方法。

BaseClassName（示例中的基类名）必须与派生类定义在一个作用域内。除了类，还可以用表达式，基类定义在另一个模块中时这一点非常有用:      
`class DerivedClassName(modname.BaseClassName):`


```python
#类定义
class people(object):
    #定义基本属性
    name = ''
    age = 0
    #定义私有属性,私有属性在类外部无法直接进行访问
    __weight = 0
    #定义构造方法
    def __init__(self,n,a,w):
        self.name = n
        self.age = a
        self.__weight = w
    def speak(self):
        print("%s 说: 我 %d 岁。" %(self.name,self.age))
#单继承示例
class student(people):
    grade = ''
    def __init__(self,n,a,w,g):
        #调用父类的构函
        people.__init__(self,n,a,w)
        self.grade = g
    #覆写父类的方法
    def speak(self):
        print("%s 说: 我 %d 岁了，我在读 %d 年级"%(self.name,self.age,self.grade))

s = student('ken',10,60,3)
s.speak()
```

    ken 说: 我 10 岁了，我在读 3 年级
    

## 方法重写
如果你的父类方法的功能不能满足你的需求，你可以在子类重写你父类的方法，实例如下：


```python
class Parent(object):        # 定义父类
    def myMethod(self):
        print ('调用父类方法')

class Child(Parent): # 定义子类
    def myMethod(self):
        print ('调用子类方法')

c = Child()          # 子类实例
c.myMethod()         # 子类调用重写方法
```

    调用子类方法
    

## 例子


```python
class Animal(object):
    def __init__(self,*args,**kwargs):
        pass
    def eat(self):
        print('Animal is eating')
    def reproduce(self):
        print('Animal is reproducing')
    
class Bird(Animal):
    def __init__(self,*args,**kwargs):
        Animal.__init__(self,*args,**kwargs)
    def fly(self):
        print('Bird is flying')
    def reproduce(self):     # 方法的重写
        print('Bird is reproducing')

class Dog(Animal):
    def __init__(self,*args,**kwargs):
        Animal.__init__(self,*args,**kwargs)
    def run(self):
        print('Dog is running')
    def eat(self):
        print('Bird is eating')
```


```python
# 多重继承
class Sound(object):
    def sound(self,voice):
        print(voice)
        
class Movement(object):
    def move(self,target_x,target_y):
        self.x,self.y=target_x,target_y
        
class Bird(Sound,Movement):
    pass

class Car(Sound,Movement):
    pass
```

# 多态

**动态类型:**一个引用可以绑定任意类型的对象。

## 运算符重载
Python同样支持运算符重载，我么可以对类的专有方法进行重载，实例如下：


```python

class Vector(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b
 
    def __str__(self):
        return 'Vector (%d, %d)' % (self.a, self.b)
   
    def __add__(self,other):
        return Vector(self.a + other.a, self.b + other.b)

v1 = Vector(2,10)
v2 = Vector(5,-2)
print (v1 + v2)
```

    Vector (7, 8)