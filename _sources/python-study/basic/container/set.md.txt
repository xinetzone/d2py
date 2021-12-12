# 集合

- set()    可变集合
- frozen() 不可变集合

集合的元素必须是不可变对象（如字符串，元组等）,且元素间有互异性。


```python
set('Hello')
```




    {'H', 'e', 'l', 'o'}



## 集合的基本操作

- **与序列一样拥有len(),min(),max()函数**

- **add方法，添加元素**


```python
s=set(['Python','is','a','magic','language'])
print(s)
```

    {'a', 'magic', 'Python', 'language', 'is'}
    


```python
s.add('!')
s
```




    {'!', 'Python', 'a', 'is', 'language', 'magic'}



也支持更新（update）


```python
a=set([1,2,3,4])
b=set([3,4,5,6])
a.update(b)
a
```




    {1, 2, 3, 4, 5, 6}



- **remove方法删除集合中元素**


```python
s=set('hello')
s
```




    {'e', 'h', 'l', 'o'}




```python
s.remove('h')
```


```python
s
```




    {'e', 'l', 'o'}



使用remove方法，若元素不存在，则会引发错误，而discard则不会。


```python
s.discard('om')
```

## 集合的特殊操作

### 等价(==) & 不等价(!=)


```python
set('Python') == set('python')
```




    False




```python
set('Python') != set('python')
```




    True



### 子集 & 超集
```
<,<=,>,>=   用来判断前面一个集合是否是后面一个集合的严格子集，子集，严格超集，超集
```


```python
set('Hello') < set('HelloWorld')
```




    True




```python
set('Hello') <= set('Hello')
```




    True




```python
set('Hello') < set('Hello')
```




    False



### 并($\bigcup$) ：使用  `|`


```python
set('Hello') | set('world')
```




    {'H', 'd', 'e', 'l', 'o', 'r', 'w'}



### 交($\bigcap$)：使用    `&`


```python
set('Hello') & set('world')
```




    {'l', 'o'}



### 差(-) ：使用   `-`


```python
set('Hello') - set('world')
```




    {'H', 'e'}



### 对称差： 使用    ` ^ `


```python
set([1,2,3,4])^set([3,4,5,6])
```




    {1, 2, 5, 6}



## Notes:

- 如是可变集合(set)与不可变集合 (frozenset)  进行运算，得到的新集合的类型与左操作数相同。        
对于可变集合(set)可以进行就地修改：    
    -  操作符为：`|=,&=,-=,^=`
- 集合只能包含不可变的 (即可散列的) 对象类型。



```python
a=set('Hello')
a |= set('Python')
a
```




    {'H', 'P', 'e', 'h', 'l', 'n', 'o', 't', 'y'}




```python
a=set('Hello')
a &= set('Python')
a
```




    {'o'}




```python
a=set('Hello')
a -= set('Python')
a
```




    {'H', 'e', 'l'}




```python
a=set('Hello')
a ^= set('Python')
a
```




    {'H', 'P', 'e', 'h', 'l', 'n', 't', 'y'}




```python
b=set('Hello')|frozenset('Python')
b
```




    {'H', 'P', 'e', 'h', 'l', 'n', 'o', 't', 'y'}




```python
c=frozenset('Python')|set('Hello')
c
```




    frozenset({'H', 'P', 'e', 'h', 'l', 'n', 'o', 't', 'y'})