
# 异常（draft）

try语句按照如下方式工作；
- 首先，执行try子句（在关键字try和关键字except之间的语句）
- 如果没有异常发生，忽略except子句，try子句执行后结束。
- 如果在执行try子句的过程中发生了异常，那么try子句余下的部分将被忽略。如果异常的类型和 except 之后的名称相符，那么对应的except子句将被执行。最后执行 try 语句之后的代码。
- 如果一个异常没有与任何的except匹配，那么这个异常将会传递给上层的try中。

一个 try 语句可能包含多个except子句，分别来处理不同的特定的异常。最多只有一个分支会被执行。   
处理程序将只针对对应的try子句中的异常进行处理，而不是其他的 try 的处理程序中的异常。      
一个except子句可以同时处理多个异常，这些异常将被放在一个括号里成为一个元组，

Python 中（至少）有两种错误：语法错误和异常(syntax errors 和 exceptions)
语法错误，也被称作解析错误


```python
while True print('Hello world')
```


      File "<ipython-input-2-614901b0e5ee>", line 1
        while True print('Hello world')
                       ^
    SyntaxError: invalid syntax
    


语法分析器指出错误行，并且在检测到错误的位置前面显示一个小“箭头”。 错误是由箭头前面的标记引起的（或者至少是这么检测的）


```python
5/0
```


    ---------------------------------------------------------------------------

    ZeroDivisionError                         Traceback (most recent call last)

    <ipython-input-1-67a69f72677d> in <module>()
    ----> 1 5/0
    

    ZeroDivisionError: division by zero



```python
try:
    print(5/0)
except ZeroDivisionError:
    print("You can't divide zero!")
```

    You can't divide zero!
    


```python
print("Give me two numbers,and I'll divide them.")
print("Enter'q' to quit.")

while True:
    first_number = input('\nFist number: ')
    if first_number == 'q':
        break
    second_number = input('\nsecond number: ')
    if second_number == 'q':
        break
    answer = int(first_number) / int(second_number)
    print(answer)
```

    Give me two numbers,and I'll divide them.
    Enter'q' to quit.
    
    Fist number: 5
    
    second number: 0
    


    ---------------------------------------------------------------------------

    ZeroDivisionError                         Traceback (most recent call last)

    <ipython-input-4-c303f6ef9aca> in <module>()
          9     if second_number == 'q':
         10         break
    ---> 11     answer = int(first_number) / int(second_number)
         12     print(answer)
    

    ZeroDivisionError: division by zero



```python
# 异常
print("Give me two numbers,and I'll divide them.")
print("Enter'q' to quit.")

while True:
    first_number = input('\nFist number: ')
    if first_number == 'q':
        break
    second_number = input('\nsecond number: ')
    if second_number == 'q':
        break
    try:
        answer = int(first_number) / int(second_number)
    except ZeroDivisionError:
        print("You can't divide zero!")
    else:
        print(answer)
```

    Give me two numbers,and I'll divide them.
    Enter'q' to quit.
    
    Fist number: 5
    
    second number: 0
    You can't divide zero!
    
    Fist number: 5
    
    second number: 3
    1.6666666666666667
    
    Fist number: q
    

# 异常

**异常**：即程序运行时遇到非正常的情况，如符号错误，逻辑错误，语法错误等等。     
python语言使用**异常对象(exception object)**来表示异常情况，由于它是一种面向对象语言，因此程序中抛出的异常也是一种类，所有的异常都是从基类Exception继承而来，而且是在Exceptions模块中被定义。Python将所有异常名称放在内建的命名空间中，使用者在使用异常时不需要导入任何模块。若异常出现时程序没有进行捕捉或处理，在程序中会使用回溯(Traceback)来终止执行。

异常有两种激活方式：
- 在程序运行出错时自动引发
- 程序员自己引发，即**抛出异常**

# 抛出异常

抛出异常往往是程序自动根据错误特征进行自动识别和抛出，在python中可以使用**raise语句**强制抛出异常。

## raise语句

当程序员想要抛出一个异常时，直接在raise语句中指明错误或异常的名称即可。

用法：     
`raise [SomeException [,arg[,traceback]]`

- SomeException是引发异常的名字，它必须是一个异常类，或异常类的实例；
- args(可选参数)传递给SomeException的参数，可以是元组或者是一个单独的对象。(因为异常参数只能为元组，所以当args是一个单独的对象，传入时会生成一个只有一个元素的元组)
- traceback(可选参数)，它是当异常触发时新生产成一个用于异常-正常化的跟踪记录对象。


```python
raise Exception
```


    ---------------------------------------------------------------------------

    Exception                                 Traceback (most recent call last)

    <ipython-input-5-fca2ab0ca76b> in <module>()
    ----> 1 raise Exception
    

    Exception: 



```python
raise NameError    # 触发类异常
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-10-0350581f77f1> in <module>()
    ----> 1 raise NameError    # 触发类异常
    

    NameError: 



```python
raise NameError() # 触发类的实例异常
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-9-1ca845d32a12> in <module>()
    ----> 1 raise NameError() # 触发类的实例异常
    

    NameError: 



```python
raise NameError("This is NameError Exception")
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-16-7324116b3e3f> in <module>()
    ----> 1 raise NameError("This is NameError Exception")
    

    NameError: This is NameError Exception



```python
raise Exception(NameError("This is NameError Exception"))
```


    ---------------------------------------------------------------------------

    Exception                                 Traceback (most recent call last)

    <ipython-input-18-da4ad2b05f15> in <module>()
    ----> 1 raise Exception(NameError("This is NameError Exception"))
    

    Exception: This is NameError Exception


## 自定义异常类

- 1)继承Exception类
- 2)使用raise语句通过人工的方式触发

示例：


```python
class CustomError(Exception):
    pass

# raise触发
raise CustomError
```


    ---------------------------------------------------------------------------

    CustomError                               Traceback (most recent call last)

    <ipython-input-19-324753841193> in <module>()
          3 
          4 # raise触发
    ----> 5 raise CustomError
    

    CustomError: 



```python
class MyError(Exception):
    def __init__(self,value):
        super(MyError,self).__init__(value)
        self.value=value
        

raise MyError("Error Information")
```


    ---------------------------------------------------------------------------

    MyError                                   Traceback (most recent call last)

    <ipython-input-21-e7eca55e3136> in <module>()
          5 
          6 
    ----> 7 raise MyError("Error Information")
    

    MyError: Error Information


# 捕获异常
目的：使程序能够不崩溃且正确运行

## try-except 语句
- 将可能出现异常的语句放到try子句；
- 将处理异常的语句放到except子句中。
```python
try:
    
    tryblock
except Exception:
    exception block
```

工作方式：      
- 首先执行try子句。若没有发生任何异常，except子句会在try子句执行完后被忽略。
- 若try子句引发异常，则try子句引发的这个异常的代码会被忽略掉。
    + 若引发的异常与except中指定的异常的类型相匹配，则会跳到except子句中执行except子句；
    + 若引发的异常在except子句中没有与之相匹配的分支，它会传递到上一级的try子句中；
    + 若仍然找不到与之匹配的except子句，它就会成为一个未处理异常，此时程序会终止运行，并且提示异常信息。
+ except子句可以没有接任何异常和异常参数，这时try语句捕获的任何异常都会交给except子句来处理。
   
示例：


```python
try:
    1/0
except ZeroDivisionError:
    print('The divisor cannot be zero')
```

    The divisor cannot be zero
    


```python
 def this_fails():
        x = 1/0

try:
    this_fails()
except ZeroDivisionError as err:
    print('Handling run-time error:', err)
```

    Handling run-time error: division by zero
    

## try-except-else 结构 

工作方式：       
- 若try范围内捕获了except语句指定的异常，就跳到except语句中继续执行；
- 若try范围内没有捕获任何异常，就执行else语句。

示例：


```python
try:
    myfile=open('myfile.txt','w')
except:
    print('myfile open failed')
else:
    print('myfile open successfully')
    myfile.close()
```

    myfile open successfully
    


```python
class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class TransitionError(Error):
    """Raised when an operation attempts a state transition that's not
    allowed.

    Attributes:
        previous -- state at beginning of transition
        next -- attempted new state
        message -- explanation of why the specific transition is not allowed
    """

    def __init__(self, previous, next, message):
        self.previous = previous
        self.next = next
        self.message = message
```

# finally语句

finally语句是指无论是否引发异常，是否被捕获都一定会执行的代码块。

## try-finally语句
这种组合其实无法捕捉异常

工作方式：    
- 若没有发生异常，则先运行try子句，然后运行finally子句；
- 若发生异常，则执行finally子句，然后把异常递交给上层try,控制流不会通过整个try语句。

类似的还有：

## try-except-finally语句

 ## try-except-else-finally语句

#  finally语句的特性：

- 当在try语句中含有return语句时，执行到return并不会直接返回，而时在执行finally语句后再执行return语句；
- 有时在处理玩finally中的资源释放之后就不需要继续处理抛出的异常了，这这种情况下可以考虑在finally语句块中使用return语句。

# 处理异常的特殊方法

## assert语句
若断言成功则不采取任何措施，否则会触发AssertionError的异常。


```python
assert 1==2,'one does not equal two!'
```


    ---------------------------------------------------------------------------

    AssertionError                            Traceback (most recent call last)

    <ipython-input-39-3ffa52fc9c11> in <module>()
    ----> 1 assert 1==2,'one does not equal two!'
    

    AssertionError: one does not equal two!


## with语句(上下文管理语句)
with语句的目的在于从流程图中把try,except和finally关键字和资源分配释放相关代码统统去掉，而不像try-except-finally那样仅仅简化代码使之易用。

- 基本用法：    
```
with context_expr[as var]:
    withblock
```
- 操作文件对象：     
```
with open(r'somefileName') as somefile:
    for line in somefile:
        print(line)
        ...
```

使用with语句，不管在处理文件过程是否发生异常，都能保证with语句执行完后已经关闭了打开的文件句柄。

with语句是一个控制流语句，它引用了一个上下文管理协议，实现方法是为一个类定义`__enter__`和`__exit__`两个函数。每次使用with语句，会首先执行`__enter__`函数，它的返回值赋值给var，当withblock执行完后，会执行`__exit__`函数。       
with语句等价与于         
```
try:
    执行__enter__函数
    执行withblock
    
finally:
    执行__exit__
```