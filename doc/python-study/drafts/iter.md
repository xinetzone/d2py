
# 迭代&生成（draft）

## 迭代器
- 迭代是Python最强大的功能之一，是访问集合元素的一种方式。
- 迭代器是一个可以记住遍历的位置的对象。
- 迭代器对象从集合的第一个元素开始访问，直到所有的元素被访问完结束。迭代器只能往前不会后退。
- 迭代器有两个基本的方法：iter() 和 next()。 

字符串，列表或元组对象都可用于创建迭代器：


```python
l=[1,2,3,4]
it = iter(l)    # 创建迭代器对象
print (next(it))   # 输出迭代器的下一个元素
print (next(it))
```

    1
    2
    


```python
l=[1,2,3,4]
it = iter(l)    # 创建迭代器对象
for x in it:
    print (x, end=" ")
```

    1 2 3 4 

也可以使用 next() 函数：


```python
import sys         # 引入 sys 模块
 
li=[1,2,3,4]
it = iter(li)    # 创建迭代器对象
 
while True:
    try:
        print (next(it))
    except StopIteration:
        sys.exit()
```

    1
    2
    3
    4
    


    An exception has occurred, use %tb to see the full traceback.
    

    SystemExit
    


    C:\Users\xiner\Anaconda3\lib\site-packages\IPython\core\interactiveshell.py:2870: UserWarning: To exit: use 'exit', 'quit', or Ctrl-D.
      warn("To exit: use 'exit', 'quit', or Ctrl-D.", stacklevel=1)
    

## 生成器

在 Python 中，使用了`yield`的函数被称为生成器（generator）。      
跟普通函数不同的是，生成器是一个返回迭代器的函数，只能用于迭代操作，更简单点理解生成器就是一个迭代器。         
在调用生成器运行的过程中，每次遇到 yield 时函数会暂停并保存当前所有的运行信息，返回yield的值。并在下一次执行 next()方法时从当前位置继续运行。


```python
import sys
 
def fibonacci(n): # 生成器函数 - 斐波那契
    a, b, counter = 0, 1, 0
    while True:
        if (counter > n): 
            return
        yield a
        a, b = b, a + b
        counter += 1
f = fibonacci(10) # f 是一个迭代器，由生成器返回生成
 
while True:
    try:
        print (next(f), end=" ")
    except StopIteration:
        sys.exit()
```

    0 1 1 2 3 5 8 13 21 34 55 


    An exception has occurred, use %tb to see the full traceback.
    

    SystemExit
    


    C:\Users\xiner\Anaconda3\lib\site-packages\IPython\core\interactiveshell.py:2870: UserWarning: To exit: use 'exit', 'quit', or Ctrl-D.
      warn("To exit: use 'exit', 'quit', or Ctrl-D.", stacklevel=1)
    

[Python yield 使用浅析](http://www.runoob.com/python3/python3-iterator-generator.html)


```python

```

# resversed(序列)   顺序翻转迭代


```python
a=list('hello')
a
```




    ['h', 'e', 'l', 'l', 'o']




```python
a1=reversed(a)    #a1是一个迭代器
```


```python
print(type(a))
print(type(a1))
```

    <class 'list'>
    <class 'list_reverseiterator'>
    


```python
b=[1,2,3,4,5]
b1=reversed(b)
```


```python
print(type(b))
print(type(b1))
```

    <class 'list'>
    <class 'list_reverseiterator'>
    


```python
reversed((1,2,4,7,8))
```




    <reversed at 0x2272e4a82e8>




```python
a2=reversed(range(5))
list(a2)
```




    [4, 3, 2, 1, 0]



# zip(序列1,序列2) 并行迭代


```python
l1=['a','b','c','d']
l2=[1,2,3,4]
list(zip(l1,l2))
```




    [('a', 1), ('b', 2), ('c', 3), ('d', 4)]




```python
l3=('a','b','c','d')
l4=[1,2,3,4]
list(zip(l1,l2))
```




    [('a', 1), ('b', 2), ('c', 3), ('d', 4)]




```python
l='hello'
s=range(len(l))
list(zip(l,s))
```




    [('h', 0), ('e', 1), ('l', 2), ('l', 3), ('o', 4)]




```python
l=dict(keys=l,values=s)
l
```




    {'keys': 'hello', 'values': range(0, 5)}




```python
s
```




    range(0, 5)




```python
list(zip(l,s))
```




    [('keys', 0), ('values', 1)]



## 编号迭代

enumerate(序列)：给序列打上编号


```python
l=['1','b','h',8]
s=enumerate(l)
s
```




    <enumerate at 0x2272dc60b88>




```python
list(s)
```




    [(0, '1'), (1, 'b'), (2, 'h'), (3, 8)]


## 循环控制语句
break & continue

- break结束当前循环，然后跳到循环后的下一条语句。
- continue提前结束当前这次循环，且继续进行下一次循环。

```python
a,b=0,1
while True:
    a,b=b,a+b
    if b>1000:
        break
print(a)
```


    987
    



```python
# (数值之和小于100的行)的奇树数值之和
m=[[12,13,20,9,30,7],[11,22,33,21,44],[30,32,25,66,1],[12,34,56,7]]
result=0
for l in m:
    tmp=0
    for n in l:
        tmp+=n
        if tmp>=100:
            break
    if tmp>=100:
        continue
    for n in l:
        if n % 2==1:
            result+=n
print(result)
```


    29
    


## else子句

**`flag` 变量可用来指示某一个特定事件是否已经发生，或某个特定状态是否存在。**

若需要在循环之后判断该条件是否符合，则需要额外的标识来记录。    
示例：

```python
l=[2,4,8,0,10,12]
flag=False
for n in l:
    if n%2==1:
        flag=True
        break
if not flag:
    print('All num is even')
```


    All num is even
    


与下面的`else子句`等价

```python
l = [2, 4, 8, 0, 10, 12]
for n in l:
    if n % 2 == 1:
        flag = True
        break
else:
    print('All num is even')
```


    All num is even
    


## 列表推导式
利用其他集合类对象（列表，元组，集合，字典，...)来创建新的列表的方法：          
示例：

```python
[2 * x for x in range(10)]
```


    [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]





```python
[2 * x for x in range(10) if x % 3 == 0]
```


    [0, 6, 12, 18]





```python
[(x, y) for x in range(2) for y in range(3)]
```


    [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]




## 字典推导式

```python
a = ('a','b','c','df','gh')
b = ['sdd',1,2,3,4,5]
d = {a[i]:b[i] for i in range(len(a))}
d
```


    {'a': 'sdd', 'b': 1, 'c': 2, 'df': 3, 'gh': 4}




## 元组推导式(迭代器)

```python
a = (x**2 for x in range(10))
type(a)
```


    generator