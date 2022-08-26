# 网络

## 套接字
Python 提供了两个级别访问的网络服务。：
- 低级别的网络服务支持基本的 Socket，它提供了标准的 BSD Sockets API，可以访问底层操作系统Socket接口的全部方法。
- 高级别的网络服务模块 SocketServer， 它提供了服务器中心类，可以简化网络服务器的开发。

Socket又称"套接字"，应用程序通常通过"套接字"向网络发出请求或者应答网络请求，使主机间或者一台计算机上的进程间可以通讯。     
Python 中，我们用 `socket()`函数来创建套接字，语法格式如下：     
`socket.socket([family[, type[, proto]]])`    
参数:
- `family`: 套接字家族可以使`AF_UNIX`或者`AF_INET`；`AF_INET`指定使用IPv4协议，如果要用更先进的IPv6，就指定为`AF_INET6`。
- `type`: 套接字类型可以根据是面向连接的还是非连接分为`SOCK_STREAM`或`SOCK_DGRAM`；`SOCK_STREAM`指定使用面向流的`TCP协议`。
- `protocol`: 一般不填默认为`0`.

Socket 对象(内建)方法
### 服务器端套接字

|函数|描述|
|:-|:-|:-|
|`s.bind()`|绑定地址`（host,port）`到套接字， 在`AF_INET`下,以元组`（host,port）`的形式表示地址。|
|`s.listen()`|开始TCP监听。backlog指定在拒绝连接之前，操作系统可以挂起的最大连接数量。该值至少为1，大部分应用程序设为5就可以了。|
|`s.accept()`|被动接受TCP客户端连接,(阻塞式)等待连接的到来|

### 客户端套接字

|函数|描述|
|:-|:-|:-|
|`s.connect()`|主动初始化TCP服务器连接，。一般`address`的格式为元组`(hostname,port)`，(port指端口号)如果连接出错，返回`socket.error`错误。|
|`s.connect_ex()`|`connect()`函数的扩展版本,出错时返回出错码,而不是抛出异常|

### 公共用途的套接字函数

|函数|描述|
|:-|:-|:-|
|`s.recv()`|接收TCP数据，数据以字符串形式返回，`bufsiz`e指定要接收的最大数据量。`flag`提供有关消息的其他信息，通常可以忽略。|
|`s.send()`|发送TCP数据，将string中的数据发送到连接的套接字。返回值是要发送的字节数量，该数量可能小于string的字节大小。|
|`s.sendall()`|完整发送TCP数据，完整发送TCP数据。将string中的数据发送到连接的套接字，但在返回之前会尝试发送所有数据。成功返回None，失败则抛出异常。|
|`s.recvform()`|接收UDP数据，与`recv()`类似，但返回值是`（data,address）`。其中`data`是包含接收数据的字符串，`address`是发送数据的套接字地址。|
|`s.sendto()`|发送UDP数据，将数据发送到套接字，`address`是形式为`（ipaddr，port）`的元组，指定远程地址。返回值是发送的字节数。|
|`s.close()`|关闭套接字|
|`s.getpeername()`|返回连接套接字的远程地址。返回值通常是元组`（ipaddr,port）`|
|`s.getsockname()`|返回套接字自己的地址。通常是一个元组`(ipaddr,port)`|
|`s.setsockopt(level,optname,value)`|设置给定套接字选项的值。|
|`s.getsockopt(level,optname[.buflen])`|返回套接字选项的值。|
|`s.settimeout(timeout)`|设置套接字操作的超时期，`timeout`是一个浮点数，单位是秒。值为`None`表示没有超时期。一般，超时期应该在刚创建套接字时设置，因为它们可能用于连接的操作（如`connect()`）|
|`s.gettimeout()`|返回当前超时期的值，单位是秒，如果没有设置超时期，则返回`None`。|
|`s.fileno()`|返回套接字的文件描述符。|
|`s.setblocking(flag)`|如果flag为0，则将套接字设为非阻塞模式，否则将套接字设为阻塞模式（默认值）。非阻塞模式下，如果调用`recv()`没有发现任何数据，或`send()`调用无法立即发送数据，那么将引起`socket.error`异常。|
|`s.makefile()`|创建一个与该套接字相关连的文件|


```python
# 导入socket库:
import socket

# 创建一个socket:
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接:
s.connect(('www.sina.com.cn', 80))
```

### 客户端
客户端要主动发起TCP连接，必须知道服务器的`IP地址`和`端口号`。新浪网站的IP地址可以用`域名www.sina.com.cn`自动转换到IP地址

80端口是Web服务的标准端口。其他服务都有对应的标准端口号，例如SMTP服务是25端口，FTP服务是21端口，等等。端口号小于1024的是Internet标准服务的端口，端口号大于1024的，可以任意使用。

因此，我们连接新浪服务器的代码如下：    
`s.connect(('www.sina.com.cn', 80))`      
建立TCP连接后，我们就可以向新浪服务器发送请求，要求返回首页的内容：


```python
# 发送数据:
s.send(b'GET / HTTP/1.1\r\nHost: www.sina.com.cn\r\nConnection: close\r\n\r\n')
```




    60




```python
# 接收数据:
buffer = []
while True:
    # 每次最多接收1k字节:
    d = s.recv(1024)
    if d:
        buffer.append(d)
    else:
        break
data = b''.join(buffer)
# 关闭连接:
s.close()
```

接收数据时，调用`recv(max)`方法，一次最多接收指定的字节数，因此，在一个while循环中反复接收，直到`recv()`返回空数据，表示接收完毕，退出循环。
当我们接收完数据后，调用close()方法关闭Socket，这样，一次完整的网络通信就结束了。   
接收到的数据包括HTTP头和网页本身，我们只需要把HTTP头和网页分离一下，把HTTP头打印出来，网页内容保存到文件：


```python
(header, html) = data.split(b'\r\n\r\n', 1)
print(header.decode('utf-8'))
# 把接收的数据写入文件:
with open('sina.html', 'wb') as f:
    f.write(html)
```

    HTTP/1.1 200 OK
    Server: nginx
    Date: Tue, 22 Aug 2017 08:03:04 GMT
    Content-Type: text/html
    Content-Length: 601703
    Connection: close
    Last-Modified: Tue, 22 Aug 2017 07:58:35 GMT
    Vary: Accept-Encoding
    Expires: Tue, 22 Aug 2017 08:04:03 GMT
    Cache-Control: max-age=60
    X-Powered-By: shci_v1.03
    Age: 0
    Via: http/1.1 cnc.beixian.ha2ts4.205 (ApacheTrafficServer/4.2.1.1 [cMsSf ]), http/1.1 ctc.ningbo.ha2ts4.106 (ApacheTrafficServer/4.2.1.1 [cRs f ])
    X-Cache: MISS.205
    X-Via-CDN: f=edge,s=ctc.ningbo.ha2ts4.101.nb.sinaedge.com,c=218.75.27.189;f=Edge,s=ctc.ningbo.ha2ts4.106,c=115.238.190.101;f=edge,s=cnc.beixian.ha2ts4.213.nb.sinaedge.com,c=115.238.190.106;f=Edge,s=cnc.beixian.ha2ts4.205,c=115.238.190.101
    X-Cache: MISS.MERGE.106
    

现在，只需要在浏览器中打开这个sina.html文件，就可以看到新浪的首页了。

### 服务器：      

+ 我们使用 `socket` 模块的 `socket()` 函数来创建一个 `socket`对象。`socket` 对象可以通过调用其他函数来设置一个 `socket` 服务。
     + 通过调用 `bind(hostname, port)` 函数来指定服务的 `port`(端口)。
     + 我们调用 `socket` 对象的 `accept` 方法。该方法等待客户端的连接，并返回 `connection` 对象，表示已连接到客户端。

完整代码如下


```python
# 文件名：server.py
import threading
# 导入 socket模块
import socket

# 创建 socket 对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 


# 绑定端口
s.bind(('127.0.0.1', 1024))

# 设置最大连接数，超过后排队
s.listen(5)
print('请稍后,正在连接中...')

# 每个连接都必须创建新线程（或进程）来处理，否则，单线程在处理连接的过程中，无法接受其他客户端的连接：
def tcplink(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    sock.send(b'Welcome!')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break
        sock.send(('Hello, %s!' % data.decode('utf-8')).encode('utf-8'))
    sock.close()
    print('Connection from %s:%s closed.' % addr)
    
while True:
    # 建立客户端连接
    sock,addr = serversocket.accept()
    # 创建新线程来处理TCP连接:
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()
```

    请稍后,正在连接中...
    

- 客户端
    接下来我们写一个简单的客户端实例连接到以上创建的服务。端口号为 9999。
    `socket.connect(hosname, port )` 方法打开一个 TCP 连接到主机为 hostname 端口为 port 的服务商。连接后我们就可以从服务端后期数据，记住，操作完成后需要关闭连接。
    
完整代码如下：


```python
# 文件名：client.py

# 导入 socket模块
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接:
s.connect(('127.0.0.1', 9999))
# 接收欢迎消息:
print(s.recv(1024).decode('utf-8'))
for data in [b'Michael', b'Tracy', b'Sarah']:
    # 发送数据:
    s.send(data)
    print(s.recv(1024).decode('utf-8'))
s.send(b'exit')
s.close()
```

现在我们打开两个终端，第一个终端执行 server.py 文件      
第二个终端执行 client.py 文件

## Python Internet 模块
以下列出了 Python 网络编程的一些重要模块：

|协议|功能用处|端口号|Python 模块|
|:-|:-|:-|:-|:-|:-|
|`HTTP`|网页访问|`80`|`httplib, urllib, xmlrpclib`|
|`NNTP`|阅读和张贴新闻文章，俗称为"帖子"|`119`|`nntplib`|
|`FTP`|文件传输|`20`|`ftplib, urllib`|
|`SMTP`|发送邮件|`25`|`smtplib`|
|`POP3`|接收邮件|`110`|`poplib`|
|`IMAP4`|获取邮件|`143`|`imaplib`|
|`Telnet`|命令行|`23`|`telnetlib`|
|`Gopher`|信息查找|`70`|`gopherlib, urllib`|