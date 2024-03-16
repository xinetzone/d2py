# `pyarrow` 集成

`pyarrow` 对文件系统有自己的内部理解（{class}`pyarrow.fs.FileSystem`），并且某些功能，特别是 parquet 的加载，要求目标与其兼容。恰好的是，`pyarrow` 中文件系统接口的设计是与 `fsspec` 兼容的（这不是偶然的）。

在导入时，`fsspec` 会检查 `pyarrow` 是否存在，如果找到 `pyarrow < 2.0`，就会将其基本文件系统添加到 spec 基类的超类中。对于 `pyarrow >= 2.0`，可以将 `fsspec` 文件系统直接传递给期望 `pyarrow` 文件系统的 `pyarrow` 函数，`pyarrow` 将[自动对其进行封装](https://arrow.apache.org/docs/python/filesystems.html#using-fsspec-compatible-filesystems)。

通过这种方式，所有派生自 `fsspec` 的文件系统也都是 `pyarrow` 文件系统，并且可以被 `pyarrow` 函数使用。
