# 全屏访问

一旦用户激活了 JupyterLite 示例，就会有“在新标签页中打开”的按钮可用，该按钮将在单独的标签页中打开相同的 JupyterLite 实例。

## 自定义链接到 JupyterLite

您可以通过 `./lite/lab` 和 `./lite/retro` 的相对 URL，全屏访问 `jupyterlite-sphinx` 为您部署的 JupyterLite 实例：

- `JupyterLab`: `./lite/lab/index.html`
- `Notebook`: `./lite/tree/index.html`

如果您想在全屏 JupyterLab/Notebook 中打开特定的笔记本，您可以使用 `path` URL参数，例如 `./lite/lab/?path=my_noteboook.ipynb`。

