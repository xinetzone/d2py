# Apache Arrow

[Apache Arrow](https://arrow.apache.org/docs/index.html) 是用于内存分析（in-memory analytics）的开发平台。它包含了一套技术，使大数据系统能够快速处理和移动数据。它规定了一种标准化的、与语言无关的列式内存格式（language-independent columnar memory format），用于扁平（flat）和分层（hierarchical）数据，以便在现代硬件上进行高效的分析操作。

该项目正在开发多语言库集合，用于解决与内存内分析数据处理相关的系统问题。这包括以下主题：

- 零拷贝共享内存和基于 RPC 的数据移动
- 读取和写入文件格式（如 CSV、Apache ORC 和 Apache Parquet）
- 内存分析和查询处理

```{toctree}
intro-PyArrow
getstarted
data
compute
memory
ipc
filesystems
numpy
pandas
dlpack
parquet
dataset
cuda
Columnar
tensor
DataType
```
