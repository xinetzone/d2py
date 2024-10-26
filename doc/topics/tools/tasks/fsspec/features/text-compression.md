# 透明文本模式和压缩

如上所述，{class}`~fsspec.core.OpenFile` 类允许在二进制存储上打开文件，这些文件看起来像是文本模式，并/或在调用者和后端存储系统之间允许压缩/解压缩层。可以使用 {func}`fsspec.available_compressions`() 获取 `fsspec` 支持的编解码器列表。从用户的角度来看，这只需通过向 {func}`fsspec.open_files` 或 {func}`fsspec.open` 函数传递参数即可，然后透明地发生。