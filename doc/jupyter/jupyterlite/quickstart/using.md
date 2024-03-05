# 使用现有的 JupyterLite 部署

如果这是你第一次听说 JupyterLite，你可能想先尝试一下。

## JupyterLite 与 JupyterLab 有什么不同？

如果你正在使用 JupyterLite 网站，没有太多需要了解的。它的工作方式就像一个常规的、有服务器支持的 JupyterLab 网站，除了：

- 内核列表，通常从 _Launcher_ 中可见的不同 _Notebook_ 风味，会有所不同。参见下面的 [内核部分](#jupyterlite-kernels)。
- 你的数据被写入到浏览器存储中
  - 尽管你可能能够复制
- 除非你的数据不会离开你的浏览器...
  - 安装了扩展并将其启用，并且将数据发送到外部服务
  - 你的 _Notebook_ 包含使用浏览器的 `fetch` 机制的代码

## 使用 JupyterLite

使用 JupyterLite 很简单：只需在网络浏览器中访问部署的 URL！

有一些面向公众的 JupyterLite 实例，它们具有不同的扩展、包和内容集合：

- JupyterLite `main` 站点，基于
  [jupyterlite](https://github.com/jupyterlite/jupyterlite) 仓库的 `main` 分支构建，部署在 ReadTheDocs：
  [https://jupyterlite.rtfd.io/en/latest/try/lab](https://jupyterlite.rtfd.io/en/latest/try/lab)。
  实际上它真的紧挨着当前的文档，你可以通过页面左上角的 `Try` 按钮启动不同的界面。
- JupyterLite `demo` 仓库：
  [https://github.com/jupyterlite/demo](https://jupyterlite.github.io/demo/)。这个仓库也可以作为创建你的网站的模板，查看
  [快速入门指南](../quickstart/deploy.md) 学习如何部署你自己的网站。
- [尝试 Jupyter](https://jupyter.org/try) 部署：
  [https://jupyter.org/try-jupyter/lab/](https://jupyter.org/try-jupyter/lab/)
- [p5 笔记本](https://github.com/jtpio/p5-notebook) 是 JupyterLite 的定制版本，专注于简洁性和使用 [p5.js](https://p5js.org/) 库。

一个部署可以有一个或多个可用的应用程序。

(jupyterlite-applications)=
## 应用程序

### JupyterLab

JupyterLab 是 Project Jupyter 的下一代用户界面，提供了经典 Jupyter Notebook 的所有熟悉构建块（笔记本、文本编辑器、文件浏览器、丰富的输出等），在一个灵活而强大的用户界面中。JupyterLab 最终将取代经典的 Jupyter Notebook。

![image](https://user-images.githubusercontent.com/591645/153932638-771ca1f4-0ec0-4b77-a5d4-644748c7538e.png)

### Jupyter Notebook

Jupyter Notebook 是一个以文档为中心的 UI，用于创建、编辑和运行 Jupyter 笔记本。

![image](https://user-images.githubusercontent.com/591645/153932487-7383ced5-003d-4752-99dc-450cc780443a.png)

### REPL

`REPL` 应用是基于 JupyterLab 代码控制台的简约用户界面，它使得在浏览器中轻松执行代码成为可能。

![image](https://user-images.githubusercontent.com/591645/153935929-23a5d380-363e-490b-aabd-f0a780140588.png)

(jupyterlite-kernels)=
## Jupyter 内核

JupyterLite内核在浏览器中实现了[Jupyter Kernel Messaging][jkm]，借助于[`mock-socket`][mock-socket]和[WebAssembly][webassembly]的帮助，无需依赖任何外部基础设施。

JupyterLite的贡献者们开发和维护了以下内核：

- 基于[Pyodide][pyodide]的Python内核：
  [https://github.com/jupyterlite/pyodide-kernel](https://github.com/jupyterlite/pyodide-kernel)
- 基于[Xeus Python][xeus-python]的Python内核

还有一些第三方的浏览器内核也与JupyterLite兼容。有关更多信息，请查看此[GitHub讨论][github-discussion-kernels]。

查阅文档中的[How-to Guides](https://jupyterlite.readthedocs.io/en/stable/howto)来了解如何使用和配置内核。

[jkm]: https://jupyter-client.readthedocs.io/en/stable/messaging.html
[mock-socket]: https://github.com/thoov/mock-socket
[webassembly]: https://developer.mozilla.org/en-US/docs/WebAssembly
[github-discussion-kernels]: https://github.com/jupyterlite/jupyterlite/discussions/968
[pyodide]: https://pyodide.org
[xeus-python]: https://github.com/jupyter-xeus/xeus-python


## 文件操作

默认情况下，您在 JupyterLite 中创建的文件会存储在浏览器的本地存储（IndexedDB）中。除非它们部署在同一个域名上，并且使用相同的浏览器，否则不同 JupyterLite 网站之间不会共享这些文件。

### 上传文件

JupyterLite 支持从您的本地计算机上传文件到浏览器的本地存储。这可以通过将文件从您的本地计算机拖放到文件浏览器中，或使用文件浏览器中的“上传”按钮来实现。

例如，当您想要上传一个数据集到笔记本中使用，如 CSV 文件时，这个功能就很有用。

然而，请注意浏览器的本地存储容量是有限的，您可能无法上传大文件。但是较小的文件，大约到 50MB 应该是没有问题的。

```{note}
要了解更多关于浏览器存储限制的信息，请查看 MDN 上的 [浏览器存储][browser-storage] 参考页面。
```

[browser-storage]:
  https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria

### 访问现有文件

一些 JupyterLite 部署可能会默认提供对某些文件的访问。这些文件作为静态资源存储在服务器上，并通过 JupyterLite 文件浏览器提供给用户。它们可以被编辑，但更改不会保存回服务器。相反，就像创建新文件一样，在浏览器的本地存储中创建一个本地副本。

```{note}
如果您想恢复到原始文件，可以删除本地副本。这可以通过在文件浏览器中右键单击文件并选择 `Delete` 来实现。
```

```{note}
如果您是站点部署者，请查看 [指南](https://jupyterlite.readthedocs.io/en/stable/howto/content/files.html) 以了解如何使文件可供用户使用。
```

## 安装 JupyterLite 应用

如果浏览器和操作系统支持，JupyterLite 也可以作为应用程序安装。

当您访问 JupyterLite 网站时，可以通过点击搜索栏中的 `Install` 按钮来将其安装为应用程序：

![如何安装 JupyterLite 应用的截图](https://user-images.githubusercontent.com/591645/228767533-1535da26-7dd3-4223-9b43-62c6e65c4171.png)

```{note}
如果看不到 `Install` 按钮，请确保在其他浏览器中检查。
```

### 在 Linux 上使用 Gnome 的示例

安装后，可以通过 Gnome 的概览启动 JupyterLite 应用程序：

![如何启动 JupyterLite 应用的截图](https://user-images.githubusercontent.com/591645/175347542-f9477e79-e029-4ae0-9299-238b74a63f26.png)

然后，应用程序将在新窗口中打开，就像常规桌面应用程序一样：

![桌面版 JupyterLite 应用程序的截图](https://user-images.githubusercontent.com/591645/228768252-35ca71ba-a8ae-4261-a24b-94ab4d896279.png)

### 在 Android 上的示例

在移动设备上也可以安装 JupyterLite 应用程序。

在 Android 上，它将如下所示：

```{image} https://user-images.githubusercontent.com/591645/228768748-c053d450-2b88-45c6-84cd-76d838228fbf.png
:alt: 如何在 Android 上安装 JupyterLite 应用的截图
:height: 512px
:align: center
```

点击 `Install` 按钮后，应用程序将出现在主屏幕上：

```{image} https://user-images.githubusercontent.com/591645/228768956-374ad79e-b5ee-45da-9077-bab4b6b7fce5.png
:alt: 主屏幕上的 JupyterLite 应用程序截图
:height: 512px
:align: center
```
