# 在网站上嵌入实时 REPL

JupyterLite 默认包含基于 JupyterLab Code Console 的最小化 `REPL` 应用程序。

![image](https://user-images.githubusercontent.com/591645/153935929-23a5d380-363e-490b-aabd-f0a780140588.png)

```{hint}
查看 [快速入门指南](../quickstart/deploy.md)，了解如何部署您自己的 JupyterLite 网站并完全控制环境和安装的扩展。

下面的代码段使用面向公众的 [jupyterlite.github.io/demo](https://jupyterlite.github.io/demo) 作为示例。
```

## 在另一个网站上嵌入 REPL

一旦您准备好了一个可用的 JupyterLite 部署，您可以使用以下代码段在任何网站上嵌入 REPL：

```html
<iframe
  src="https://jupyterlite.github.io/demo/repl/index.html"
  width="100%"
  height="100%"
></iframe>
```

## 配置

可以通过 URL 参数来配置 REPL 的行为和外观。

### 默认选择内核

要避免内核选择对话框并默认选择给定的内核：

```html
<iframe
  src="https://jupyterlite.github.io/demo/repl/index.html?kernel=python"
  width="100%"
  height="100%"
></iframe>
```

### 启用工具栏

可以启用（选择加入）工具栏，以添加几个有用的按钮：

```html
<iframe
  src="https://jupyterlite.github.io/demo/repl/index.html?toolbar=1"
  width="100%"
  height="100%"
></iframe>
```

### 在启动时自动执行代码

自定义代码可以在启动时自动执行：

```html
<iframe
  src="https://jupyterlite.github.io/demo/repl/index.html?kernel=python&code=import numpy as np"
  width="100%"
  height="100%"
></iframe>
```

### 主题

还可以选择主题，例如使用 `JupyterLab Dark`：

```html
<iframe
  src="https://jupyterlite.github.io/demo/repl/index.html?theme=JupyterLab Dark"
  width="100%"
  height="100%"
></iframe>
```

如果其他主题作为 JupyterLab 预构建扩展分发，可以使用 `pip` 安装。例如：

```bash
pip install jupyterlab-gt-coar-theme
```

有关如何自定义环境以及添加更多主题和扩展的更多详细信息，请参阅 [操作指南](https://jupyterlite.readthedocs.io/en/stable/howto)。
