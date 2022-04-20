
# I/O操作（draft）

`I/O(Input/Output)`,即输入/输出。

通常程序在运行过程中，程序的中间结果和参数往往保存在内存在中，这样可以大大提高运算速度，缓解CPU于与读/写速度的不平衡造成的系统效率低下的问题。

Python的标准输入/输出为：sys.stdin  sys.stdout

## 文件
文件一般分为两种：
- 二进制文件
- ASCII(纯文本文件)

文件一般是指以文件名标识的，存储在外部介质上的一组相关数据的有序集合。
+ 文件是操作系统和用户进行数据管理的单位。
+ 文件一般存储在外部介质上，在使用时将文件调入内存。
+ 文件只是连续的字节序列。数据的传输通常使用“字节流”模式。

## 读取文件

open()返回一个文件对象，对该文件进行后继相关的操作都要用到它。

open函数提供了初始化I/O操作通用接口。

格式：
```
file_object=open(file_name,access_mode='r',buffering==-1)
```

参数简介：       
+ file_name(作为唯一的强制参数)是包含要打开的文件的字符串，它可以是绝对路径或相对路径。
+ access_mode代表文件打开的模式。(是字符串的形式)
+ buffering用于指示访问文件所采用的缓冲方式。如果buffering的值被设为0，就不会有寄存。如果buffering的值取1，访问文件时会寄存行。如果将buffering的值设为大于1的整数，表明了这就是的寄存区的缓冲大小。如果取负值，寄存区的缓冲大小则为系统默认。

文件模式：

|模式|描述|
|:-|:-|
|r|以只读方式打开文件。文件的指针将会放在文件的开头。这是默认模式。|
|w|打开一个文件只用于写入。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。|
|a|打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。|
|b|二进制模式(可添加到其他模式中使用)|
|`+`|读/写模式(可添加到其他模式中使用)|

组合形式：

|模式|描述|
|:---:|:----|
|`rb`|以二进制格式打开一个文件用于只读。文件指针将会放在文件的开头。这是默认模式。|
|`r+`|打开一个文件用于读写。文件指针将会放在文件的开头。|
|`rb+`|以二进制格式打开一个文件用于读写。文件指针将会放在文件的开头。|
|`wb`|以二进制格式打开一个文件只用于写入。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。|
|`w+`|打开一个文件用于读写。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。|
|`wb+`|以二进制格式打开一个文件用于读写。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。|
|`ab`|以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。|
|`a+`|打开一个文件用于读写。如果该文件已存在，文件指针将会放在文件的结尾。文件打开时会是追加模式。如果该文件不存在，创建新文件用于读写。|
|`ab+`|以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。如果该文件不存在，创建新文件用于读写。|


```python
test_file=open('C:/Users/xiner/学习/test.txt')
```


```python
text=test_file.read()
```


```python
print(text)
```

    啊飒飒
    sddds
    s打广告
    

## 文件方法

|方法|描述|
|:-|:-|
|file.close()|关闭文件。关闭后文件不能再进行读写操作。|
|file.flush()|刷新文件内部缓冲，直接把内部缓冲区的数据立刻写入文件, 而不是被动的等待输出缓冲区写入。|
|file.fileno()|返回一个整型的文件描述符(file descriptor FD 整型), 可以用在如os模块的read方法等一些底层操作上。|
|file.isatty()|如果文件连接到一个终端设备返回 True，否则返回 False。|
|file.next()|返回文件下一行。|
|file.read([size])|从文件读取指定的字节数，如果未给定或为负则读取所有。|
|file.readline([size])|读取整行，包括 "\n" 字符。|
|file.readlines([sizehint])|读取所有行并返回列表，若给定sizeint>0，返回总和大约为sizeint字节的行, 实际读取值可能比sizhint较大, 因为需要填充缓冲区。|
|file.seek(offset[, whence])|设置文件当前位置|
|file.tell()|返回文件当前位置。|
|file.truncate([size])|截取文件，截取的字节通过size指定，默认为当前文件位置。| 
|file.write(str)|将字符串写入文件，没有返回值。|
|file.writelines(sequence)|向文件写入一个序列字符串列表，如果需要换行则要自己加入每行的换行符。|


```python
test_file1=open('C:/Users/xiner/学习/myfile.txt','w')   #写入新的文件
```


```python
test_file1.write('This is my test file')
test_file1.close()
```


```python
test_file1=open('C:/Users/xiner/学习/myfile.txt')
text1=test_file1.read()
text1
```




    'This is my test file'




```python
# stdin.py
print('hello world!')
user=input('Please enter your name:')
print('Hi,%s!'%user)
```

    hello world!
    Please enter your name:T
    Hi,T!
    


```python
%pwd  # 文件目录
```




    'C:\\Users\\xiner\\学习'




```python
#打开文件
fo=open('foo.txt','wb')
print('Name of the file:',fo.name)
# 关闭文件
fo.close()
```

    Name of the file: foo.txt
    



```python
## 上下文管理模式
with open('pi_dights.txt') as file_object:
    print(file_object.read())
```

    3.1415926535
      8979311599
      7963468544
    0x1A0x1A
    

## 处理二进制文件

ASCII可以使用任何文字处理程序阅读，且其编码是基于字符定长的，译码相对容易些；   
而二进制文件编码是不定长的，灵活利用率高，译码要难些。
- 使用'r'时若碰到'0x1A',就会视为文件结束，即EOF；但是使用'rb'则不会存至在此问题。

## python使用struct模块来处理二进制数据

- `pack(fmt,v1,v1,...)`：    
按照给定的格式(`fmt`),把数据封装成字符串(类似于C结构体的字节流)
+ `unpack(fmt,string)`：       
按照给定的格式(`fmt`)解析字节流`string`，返回解析出来的`tuple`
+ `calcsize(fmt)`：    
计算给定的格式(`fmt`)占用多少字节的内存


```python
 import struct
a=20
b=400
st=struct.pack('ii',a,b)  #转换成字节流，虽然还是字符串，但是可以在网络上传输
print(len(st))
print(st)
print(repr(st))
```

    8
    b'\x14\x00\x00\x00\x90\x01\x00\x00'
    b'\x14\x00\x00\x00\x90\x01\x00\x00'
    


```python
import struct
a = b'hello'
b = b'world!'
c = 2
d = 45.123
t = struct.pack('5s6sif',a,b,c,d)
s = struct.unpack('5s6sif',t)
print(t)
print(s)
```

    b'helloworld!\x00\x02\x00\x00\x00\xf4}4B'
    (b'hello', b'world!', 2, 45.12300109863281)
    

struct中支持的格式如下表：

|Format|C Type|Python|字节数|
|:-|:-|:-|:-|
|x|pad byte|no value|1|
|c|char|string of length 1|1|
|b|signed char|integer|1|
|B|unsigned char|integer|1|
|`?`|`_`Bool|bool|1|
|h|short|integer|2|
|H|unsigned short|integer|2|
|i|int|integer|4|
|I|unsigned int|integer or long|4|
|l|long|integer|4|
|L|unsigned long|long|4|
|q|long long|long|8|
|Q|unsigned long long|long|8|
|f|float|float|4|
|d|double|float|8|
|s|char[]|string|1|
|p|char[]|string|1|

- 注1.q和Q只在机器支持64位操作时有意思
- 注2.每个格式前可以有一个数字，表示个数
- 注3.s格式表示一定长度的字符串，4s表示长度为4的字符串，但是p表示的是pascal字符串
- 注4.P用来转换一个指针，其长度和机器字长相关
- 注5.最后一个可以用来表示指针类型的，占4个字节

为了同c中的结构体交换数据，还要考虑有的c或c++编译器使用了字节对齐，通常是以4个字节为单位的32位系统，故而struct根据本地机器字节顺序转换.可以用格式中的第一个字符来改变对齐方式.定义如下：

|Character|Byte order|Size and alignment|
|:-|:-|:-|
|`@`|native|native            凑够4个字节|
|`=`|native|standard        按原字节数|
|`<`|little-endian|standard        按原字节数|
|`>`|big-endian|standard       按原字节数|
|`!`|network (= big-endian)|standard       按原字节数|
使用方法是放在fmt的第一个位置，就像`'@5s6sif'`


```python
import struct
#native byteorder
buffer=struct.pack('ihb',1,2,3) #将二进制数据分装成字符串
print(repr(buffer))
print(struct.unpack('ihb',buffer)) #将字符串反解析成数据

# data from a sequence,network byteorder
data=[1,2,3]
buffer=struct.pack('!ihb',*data) #将数据按照大端格式转换
print(repr(buffer))
print(struct.unpack('!ihb',buffer))
```

    b'\x01\x00\x00\x00\x02\x00\x03'
    (1, 2, 3)
    b'\x00\x00\x00\x01\x00\x02\x03'
    (1, 2, 3)
    


```python
def add_some_text():
    f=open(r'C:\Users\xiner\AnacondaProjects','a')
    f.write('Here is some text!')
    f.close()
```

## os模块

[Python3 OS 文件/目录方法](http://www.runoob.com/python3/python3-os-file-methods.html)


```python

```