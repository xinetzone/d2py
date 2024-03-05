# `jupyterlite-sphinx` 用法

`jupyterlite-sphinx` 提供了一组指令，允许您直接在文档页面中嵌入不同的 JupyterLite UI。
这些指令可以使用以下选项进行配置：

- `width`（默认值为 `"100%"`）UI 的宽度
- `height`（默认值为 `"600px"`）UI 的高度
- `theme`（默认值为 `None`）要使用的 JupyterLab 主题
- `prompt`（默认值为 `False`）是否懒加载 UI。如果该值为字符串，则将其用作提示按钮的值。
- `prompt_color`（默认值为 `#f7dc1e`）提示按钮的颜色（如果有的话）。

```{toctree}
:maxdepth: 2

directives/index
full
```
