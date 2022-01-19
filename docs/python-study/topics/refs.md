# 临时区

- {mod}`计算差异的辅助工具 <difflib>`
- {mod}`文件及目录的比较 <filecmp>`
- {daobook}`日志操作手册 <cpython/howto/logging-cookbook.html>`
- [CVPR 2021 | TCANet：最强时序动作提名修正网络解读【Arxiv链接已更新】](https://zhuanlan.zhihu.com/p/358754602) & https://github.com/daobook/Temporal-Context-Aggregation-Network-Pytorch
- {mod}`操作类似图的结构的功能 <graphlib>`
- [Practical Python Projects](https://yasoob.me/posts/practical-python-projects-book-released/)
- [Python Tips](https://book.pythontips.com/en/latest/index.html)



Python有“自带电池”的理念。通过其包的复杂和强大功能可以最好地看到这一点。例如:


Python有“自带电池”的理念。通过其包的复杂和强大功能可以最好地看到这一点。例如:

- {mod}`xmlrpc.client` 和 {mod}`xmlrpc.server` 模块使得实现远程过程调用变成了小菜一碟。尽管存在于模块名称中，但用户不需要直接了解或处理 XML。

- {mod}`email` 包是一个用于管理电子邮件的库，包括 MIME 和其他符合 RFC 2822 规范的邮件文档。与 {mod}`smtplib` 和 {mod}`poplib` 不同（它们实际上做的是发送和接收消息），电子邮件包提供完整的工具集，用于构建或解码复杂的消息结构（包括附件）以及实现互联网编码和标头协议。

- {mod}`json` 包为解析这种流行的数据交换格式提供了强大的支持。{mod}`csv` 模块支持以逗号分隔值格式直接读取和写入文件，这种格式通常为数据库和电子表格所支持。 XML 处理由 {class}`xml.etree.ElementTree`，{mod}`xml.dom` 和 {mod}`xml.sax` 包支持。这些模块和软件包共同大大简化了 Python 应用程序和其他工具之间的数据交换。
- {mod}`sqlite3` 模块是 SQLite 数据库库的包装器，提供了一个可以使用稍微非标准的 SQL 语法更新和访问的持久数据库。
- 国际化由许多模块支持，包括 {mod}`gettext`， {mod}`locale`，以及 {mod}`codecs` 包。