# 在独立服务器或本地部署 JupyterLite

部署 JupyterLite 站点需要：

- 一份 JupyterLite 站点资源副本
  - 通常由可安装的 `pip` python 包 `jupyterlite-core` 提供
- 一组可选的站点和不同应用程序的配置
  - 不同的选项在可复制性、构建速度、部署大小以及最终用户的性能、隐私和安全之间提供了权衡

## 获取空的 JupyterLite 站点

最小的可部署站点档案包含运行所有默认 [应用程序](jupyterlite-applications) 所需的一切，但没有内容。

```{hint}
使用命令行界面是可选的，但是 **推荐的**。它与其他 Jupyter 工具的集成要好得多。
```

要从 [PyPI] 获取 [Python CLI](https://pypi.org/project/jupyterlite/) 和 [API](https://jupyterlite.readthedocs.io/en/stable/reference/api/index.html)：

```bash
python -m pip install jupyterlite-core
```

您还可以使用 `conda` 从 [conda forge] 安装 CLI：

```bash
conda install -c conda-forge jupyterlite-core
```

或者 `mamba`:

```bash
mamba install -c conda-forge jupyterlite-core
```

构建空站点（仅包含 JupyterLite 静态资源）：

```bash
jupyter lite init
```

默认情况下，JupyterLite 网站将被放置在 `_output` 文件夹中。您可以使用 `--output-dir` 参数指定不同的文件夹。例如：

```bash
jupyter lite build --output-dir dist
```

````{note}
默认情况下，`jupyterlite-core` 包不提供任何内核。如果您希望在您的环境安装一个内核，您需要在构建环境中安装它。例如，要为 JupyterLite 安装 Pyodide 内核：

```bash
python -m pip install jupyterlite-pyodide-kernel
```

然后确保重新运行 `jupyter lite build` 命令。
````

## 自定义站点

默认情况下，JupyterLite 站点将是空的，但您可以通过添加自己的内容和配置来自定义它。

文档包括几个如何自定义站点的指南：

- [添加内核](https://jupyterlite.readthedocs.io/en/stable/howto/configure/kernels.html)
- [添加扩展](https://jupyterlite.readthedocs.io/en/stable/howto/configure/simple_extensions.html)
- [添加内容](https://jupyterlite.readthedocs.io/en/stable/howto/content/files.html)

查看 [如何指南列表](https://jupyterlite.readthedocs.io/en/stable/howto) 以获取更多信息。

## 独立服务器

现在静态资源已经构建完成，您可以使用一个普通的 HTTP 服务器来提供它们，并通过网络浏览器访问 JupyterLite。

适用于本地开发，许多语言提供了易于使用的服务器，可以在您使其按您想要的方式工作时在本地提供 JupyterLite。

```{warning}
提供某些内核需要您的 web 服务器支持
使用正确的头部提供 `application/wasm` 文件
```

```{hint}
推荐使用支持 HTTPS 的服务器，除非是最简单的 `localhost` 情况。
```

### `jupyter lite serve`

`jupyter lite serve` 命令提供了一个由 Python 内置的 `http.server` 或 `tornado` 提供支持的 web 服务器，如果安装了任何其他 Jupyter 工具，`tornado` 可能会可用。

在同一目录下，运行以下命令启动服务器：

```bash
jupyter lite serve
```

```{note}
还有更多选项可用，例如更改端口和日志级别。
使用 `jupyter lite serve --help` 查看帮助以了解更多信息。
```

#### Jupyter

如果您已经在运行由 [Jupyter Server] 提供支持的应用程序，例如 JupyterLab，那么您的文件将通过例如 `http://localhost:8888/files` 正确提供服务。

#### Python

##### http.server

Python 标准库中的 `http` 模块是一个适合本地用途的有效服务器。

```bash
python -m http.server -b 127.0.0.1
```

如果您使用的是最近发布的 Python 3.7+，这将正确提供 WebAssembly 内核的 `application/wasm` 文件。

#### NodeJS

大多数基于 nodejs 的服务器将能够毫无问题地托管 JupyterLite。然而，请注意，`http-server` 不支持 `application/wasm` MIME 类型。

## 使用发布存档

作为使用 `jupyter-lite` CLI 的替代方法，您也可以从 [GitHub Releases][releases] 页面下载发布存档。

下载并解压它，然后使用上述提到的方法之一启动服务器。

从 [GitHub actions] 也可获取每日构建和正在进行中的存档。

[github actions]: https://github.com/jupyterlite/jupyterlite/actions
[releases]: https://github.com/jupyterlite/jupyterlite/releases
[pypi]: https://pypi.org/project/jupyterlite/
[conda forge]: https://conda-forge.org/
[jupyter server]: https://jupyter-server.readthedocs.io/en/latest/
