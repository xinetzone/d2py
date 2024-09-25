# 配置

JupyterLite-sphinx 可以通过在 `conf.py` 文件中设置一些全局 Python 变量来进行配置：

## JupyterLite 内容

您可以通过提供以下配置，在 JupyterLite 构建中嵌入自定义内容（笔记本和数据文件）：

```python
jupyterlite_contents = ["./path/to/my/notebooks/", "my_other_notebook.ipynb"]
```
`jupyterlite_contents` 可以是字符串或字符串列表。每个字符串都使用 Python 的 `glob.glob` 函数进行扩展，并使用其递归选项。有关更多详细信息，请参见 [glob 文档](https://docs.python.org/3/library/glob.html#glob.glob) 和 [通配符模式文档](https://docs.python.org/3/library/fnmatch.html#fnmatch.fnmatch)。

## JupyterLite 目录

默认情况下，`jupyterlite-sphinx` 会在文档目录中运行 `jupyter lite build` 命令，您可以覆盖此行为并要求 `jupyterlite` 在给定目录中构建：

```python
# Build in the current directory
jupyterlite_dir = "/path/to/your/lite/dir"
```

## 预安装的包

为了在内核环境中预安装 Python 包，您可以使用 [jupyterlite-xeus](https://jupyterlite-xeus.readthedocs.io)，并使用 `xeus-python` 内核。

您需要在文档构建环境中安装 `jupyterlite-xeus`。

您可以通过在文档目录中添加 `environment.yml` 文件来预安装包，其中将 `xeus-python` 定义为依赖项之一。它将在运行 `jupyter lite build` 时预构建环境。

此外，这会自动安装它找到的任何 labextension，例如安装 ipyleaflet 将使 ipyleaflet 无需手动安装 jupyter-leaflet labextension 即可工作。

假设您想要安装 NumPy、Matplotlib 和 ipycanvas，可以通过创建具有以下内容的 environment.yml 文件来完成：

```yaml
name: xeus-python-kernel
channels:
  - https://repo.mamba.pm/emscripten-forge
  - https://repo.mamba.pm/conda-forge
dependencies:
  - numpy
  - matplotlib
  - ipycanvas
```

## JupyterLite 配置

您可以为您的 JupyterLite 部署提供 [自定义配置](https://jupyterlite.readthedocs.io/en/latest/howto/index.html#configuring-a-jupyterlite-deployment)。

```python
jupyterlite_config = "jupyterlite_config.json"
```

## 禁用 `.ipynb` 文档源绑定

默认情况下，`jupyterlite-sphinx` 会绑定 `.ipynb` 源后缀，以便使用 JupyterLite 渲染文档树中包含的笔记本。
众所周知，这可能会在使用 sphinx-gallery 等插件时产生警告，或与 nbsphinx 发生冲突。

您可以通过设置以下配置来禁用此行为：

```python
jupyterlite_bind_ipynb_suffix = False
```
