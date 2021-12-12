# re

## 预览
### python re正则表表达式语法
1. 匹配字符
    `.`  匹配任意除换行符，也就是“\n”以外的任何字符。
    `\ ` 转义符，改变原来符号含义。
    `[ ]`  中括号用来创建一个字符集，第一个出现字符如果是^，表示反向匹配。
2. 预定义字符集
    `\d`    匹配数字，如：[0-9]
    `\D`   与上面正好相反，匹配所有非数字字符。
    `\s`     空白字符，如：空格，`\t\r\n\f\v`等。
    `\S`    非空白字符。
    `\w`    单词字符，如：大写`A~Z`，小写`a~z`，数字`0~9`。
    `\W`   非上面这些字符。
3. 可选项与重复子模式
    `*`   匹配前一个字符0次或无限次数。
    `+`  匹配前一个字符1次或无限次数。
    `?`   匹配前一个字符0次或1次。
    `{m}` 匹配前一个字符m次。
    `{m,n}` 匹配前一个字符m至n次。
    
### re模块重要函数变量
1. compile() 根据正则表达式字符串，创建模式的对象。
2. search() 在字符串中寻找模式,寻找第一个匹配的正则表达式子串。(函数找到子字符串的话会返回MatchObject，值为 True，找不到会返回None，值为False。)
3. match() 在字符串开始处匹配模式。
4. split() 根据模式的匹配项来分割字符串。
5. findall() 会以列表的形式返回给定模式的所有匹配项。
6. sub(old,new) 方法的功能是，用将所有old的匹配项用new替换掉。
7. escape() 将字符串中所有特殊正则表达式字符转义。

# re.match函数
re.match 尝试从字符串的起始位置匹配一个模式，如果不是起始位置匹配成功的话，match()就返回none。        
函数语法：      
$$re.match(pattern, string, flags=0)$$

函数参数说明：

|参数|描述|
|:-:|:-:|
|pattern|匹配的正则表达式|
|string|要匹配的字符串。|
|flags|标志位，用于控制正则表达式的匹配方式，如：是否区分大小写，多行匹配等等。|

匹配成功re.match方法返回一个匹配的对象，否则返回None。      
我们可以使用group(num) 或 groups() 匹配对象函数来获取匹配表达式。

|匹配对象方法|描述|
|:-:|:-:|
|group(num=0)|匹配的整个表达式的字符串，group() 可以一次输入多个组号，在这种情况下它将返回一个包含那些组所对应值的元组。|
|groups()|返回一个包含所有小组字符串的元组，从 1 到 所含的小组号。|


```python
import re
print(re.match('www', 'www.runoob.com').span())  # 在起始位置匹配
print(re.match('com', 'www.runoob.com'))         # 不在起始位置匹配
```

    (0, 3)
    None
    


```python
import re

line = "Cats are smarter than dogs"

matchObj = re.match( r'(.*) are (.*?) .*', line, re.M|re.I)

if matchObj:
    print ("matchObj.group() : ", matchObj.group())
    print ("matchObj.group(1) : ", matchObj.group(1))
    print ("matchObj.group(2) : ", matchObj.group(2))
else:
    print ("No match!!")
```

    matchObj.group() :  Cats are smarter than dogs
    matchObj.group(1) :  Cats
    matchObj.group(2) :  smarter
    

# re.search方法
re.search 扫描整个字符串并返回第一个成功的匹配。

函数语法：
$$re.search(pattern, string, flags=0)$$
函数参数说明：

|参数|描述|
|:-|:-|
|pattern|匹配的正则表达式|
|string|要匹配的字符串。|
|flags|标志位，用于控制正则表达式的匹配方式，如：是否区分大小写，多行匹配等等。|

匹配成功re.search方法返回一个匹配的对象，否则返回None。      
我们可以使用group(num) 或 groups() 匹配对象函数来获取配表达式。

|匹配对象方法|描述|
|:-|:-|
|group(num=0)|匹配的整个表达式的字符串，group() 可以一次输入多个组号，在这种情况下它将返回一个包含那些组所对应值的元组。|
|groups()|返回一个包含所有小组字符串的元组，从 1 到 所含的小组号。|


```python
import re

print(re.search('www', 'www.runoob.com').span())  # 在起始位置匹配
print(re.search('com', 'www.runoob.com').span())         # 不在起始位置匹配
```

    (0, 3)
    (11, 14)
    


```python
import re

line = "Cats are smarter than dogs";

searchObj = re.search( r'(.*) are (.*?) .*', line, re.M|re.I)

if searchObj:
    print ("searchObj.group() : ", searchObj.group())
    print ("searchObj.group(1) : ", searchObj.group(1))
    print ("searchObj.group(2) : ", searchObj.group(2))
else:
    print ("Nothing found!!")
```

    searchObj.group() :  Cats are smarter than dogs
    searchObj.group(1) :  Cats
    searchObj.group(2) :  smarter
    

# re.match与re.search的区别
re.match只匹配字符串的开始，如果字符串开始不符合正则表达式，则匹配失败，函数返回None；而re.search匹配整个字符串，直到找到一个匹配。


```python
import re

line = "Cats are smarter than dogs";

matchObj = re.match( r'dogs', line, re.M|re.I)
if matchObj:
    print ("match --> matchObj.group() : ", matchObj.group())
else:
    print ("No match!!")

matchObj = re.search( r'dogs', line, re.M|re.I)
if matchObj:
    print ("search --> matchObj.group() : ", matchObj.group())
else:
    print ("No match!!")
```

    No match!!
    search --> matchObj.group() :  dogs
    

# 检索和替换
Python 的re模块提供了re.sub用于替换字符串中的匹配项。

语法：
$$re.sub(pattern, repl, string, count=0)$$

参数：
- pattern : 正则中的模式字符串。
- repl : 替换的字符串，也可为一个函数。
- string : 要被查找替换的原始字符串。
- count : 模式匹配后替换的最大次数，默认 0 表示替换所有的匹配。


```python
import re

phone = "2004-959-559 # 这是一个电话号码"

# 删除注释
num = re.sub(r'#.*$', "", phone)
print ("电话号码 : ", num)

# 移除非数字的内容
num = re.sub(r'\D', "", phone)
print ("电话号码 : ", num)
```

    电话号码 :  2004-959-559 
    电话号码 :  2004959559
    

## repl 参数是一个函数
以下实例中将字符串中的匹配的数字乘于 2：


```python
import re

# 将匹配的数字乘于 2
def double(matched):
    value = int(matched.group('value'))
    return str(value * 2)

s = 'A23G4HFD567'
print(re.sub('(?P<value>\d+)', double, s))
```

    A46G8HFD1134
    

# 正则表达式修饰符 - 可选标志
正则表达式可以包含一些可选标志修饰符来控制匹配的模式。修饰符被指定为一个可选的标志。多个标志可以通过按位 `OR(|) `它们来指定。如` re.I | re.M `被设置成 $I$ 和$M$标志：

|修饰符|描述|
|:-|:-|
|re.I|使匹配对大小写不敏感|
|re.L|做本地化识别（locale-aware）匹配|
|re.M|多行匹配，影响` ^ `和`$`|
|re.S|使`.`匹配包括换行在内的所有字符|
|re.U|根据Unicode字符集解析字符。这个标志影响 `\w, \W, \b, \B`.|
|re.X|该标志通过给予你更灵活的格式以便你将正则表达式写得更易于理解。|

# 正则表达式模式
```
模式字符串使用特殊的语法来表示一个正则表达式：
字母和数字表示他们自身。一个正则表达式模式中的字母和数字匹配同样的字符串。
多数字母和数字前加一个反斜杠时会拥有不同的含义。
标点符号只有被转义时才匹配自身，否则它们表示特殊的含义。
反斜杠本身需要使用反斜杠转义。
由于正则表达式通常都包含反斜杠，所以你最好使用原始字符串来表示它们。模式元素(如 r'/t'，等价于'//t')匹配相应的特殊字符。
下表列出了正则表达式模式语法中的特殊元素。如果你使用模式的同时提供了可选的标志参数，某些模式元素的含义会改变。
```

|模式|描述|
|:-|:-|
|`^`|匹配字符串的开头|
|`$`|匹配字符串的末尾。|
|`.`|匹配任意字符，除了换行符，当re.DOTALL标记被指定时，则可以匹配包括换行符的任意字符。|
|`[...]`|用来表示一组字符,单独列出：`[amk] `匹配 `'a'，'m'或'k'`|
|`[^...]`|不在`[]`中的字符：`[^abc]` 匹配除了a,b,c之外的字符。|
|`re*`|匹配0个或多个的表达式。|
|`re+`|匹配1个或多个的表达式。|
|`re?`|匹配0个或1个由前面的正则表达式定义的片段，非贪婪方式|
|`re{ n}`||
|`re{ n,}`|精确匹配n个前面表达式。|
|`re{ n, m}`|匹配 n 到 m 次由前面的正则表达式定义的片段，贪婪方式|
|`a`$\mid$`b`|匹配a或b|
|`(re)`$\mid$`G`|匹配括号内的表达式，也表示一个组|
|`(?imx)`|正则表达式包含三种可选标志：i, m, 或 x 。只影响括号中的区域。|
|`(?-imx)`|正则表达式关闭 i, m, 或 x 可选标志。只影响括号中的区域。|
|`(?: re)`|类似 `(...)`, 但是不表示一个组|
|`(?imx: re)`|在括号中使用i, m, 或 x 可选标志|
|`(?-imx: re)`|在括号中不使用i, m, 或 x 可选标志|
|`(?#...)`|注释.|
|`(?= re)`|前向肯定界定符。如果所含正则表达式，以 ... 表示，在当前位置成功匹配时成功，否则失败。但一旦所含表达式已经尝试，匹配引擎根本没有提高；模式的剩余部分还要尝试界定符的右边。|
|`(?! re)`|前向否定界定符。与肯定界定符相反；当所含表达式不能在字符串当前位置匹配时成功|
|`(?> re)`|匹配的独立模式，省去回溯。|
|`\w`|匹配字母数字|
|`\W`|匹配非字母数字|
|`\s`|匹配任意空白字符，等价于 `[\t\n\r\f]`.|
|`\S`|匹配任意非空字符|
|`\d`|匹配任意数字，等价于 `[0-9]`.|
|`\D`|匹配任意非数字|
|`\A`|匹配字符串开始|
|`\Z`|匹配字符串结束，如果是存在换行，只匹配到换行前的结束字符串。c|
|`\z`|匹配字符串结束|
|`\G`|匹配最后匹配完成的位置。|
|`\b`|匹配一个单词边界，也就是指单词和空格间的位置。例如， `'er\b'` 可以匹配"never" 中的 'er'，但不能匹配 "verb" 中的 'er'。|
|`\B`|匹配非单词边界。`'er\B'` 能匹配 "verb" 中的 'er'，但不能匹配 "never" 中的 'er'。|
|`\n`,`\t`, 等.|匹配一个换行符。匹配一个制表符。等|
|`\1...\9`|匹配第n个分组的内容。|
|`\10`|匹配第n个分组的内容，如果它经匹配。否则指的是八进制字符码的表达式。|

# 几个例子


```python
import re
```


```python
# 判断字符串是否由‘hello’开始
pattern=re.compile('hello') #得到匹配字符串‘hello’的正则表示对象
res=pattern.match('hello world') #使用match方法进行匹配
if res :
    print(res.group()) # 使用group方法得到匹配内容
else:
    print('not match')
```

    hello
    


```python
# 查找字符串是否包含'hello'
pattern=re.compile('hello') #得到匹配字符串‘hello’的正则表示对象
res=pattern.search('world hello') #使用search方法进行匹配
if res :
    print(res.group()) # 使用group方法得到匹配内容
else:
    print('not match')
```

    hello
    


```python
# 查找字符串中包含'hello'的所有部分
pattern=re.compile('hello') #得到匹配字符串‘hello’的正则表示对象
res=pattern.findall('world hello world hello') #使用findall方法得到所有匹配内容
print(res)
```

    ['hello', 'hello']
    

##  `.`


```python
import re
pattern=re.compile(r'ab.xy')
res=pattern.match(r'ab0xy')
if res:
    print(res.group())
```

    ab0xy
    

## `|`


```python
import re
pattern=re.compile(r'abc|xyz')
res=pattern.match(r'abc')
if res:
    print(res.group())
```

    abc
    


```python
res=pattern.match(r'xyz')
if res:
    print(res.group())
```

    xyz
    

## [ ]


```python
import re 
pattern=re.compile(r'[ab][xy][01]')
res=pattern.match(r'ax0')
if res:
    print(res.group())
```

    ax0
    


```python
import re
html = 'Hello <a href="https://www.biaodainfu.com">biaodianfu</a>'
m = re.findall('<a.*>.*<\/a>', html)
if m:
    print(m)
```

    ['<a href="https://www.biaodainfu.com">biaodianfu</a>']
    


```python
import re
html = 'Hello <a href="https://www.biaodainfu.com">biaodianfu</a> | Hello <a href="https://www.google.com">Google</a>'
m = re.findall('<a.*>.*<\/a>', html)
if m:
    print(m)
```

    ['<a href="https://www.biaodainfu.com">biaodianfu</a> | Hello <a href="https://www.google.com">Google</a>']