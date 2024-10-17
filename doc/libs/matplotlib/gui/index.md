# 在 GUI 中嵌入 Matplotlib

您可以通过遵循这里的 embedding_in_SOMEGUI.py 示例，将 Matplotlib 直接嵌入到用户界面应用程序中。目前 Matplotlib 支持 PyQt/PySide、PyGObject、Tkinter 和 wxPython。

当在 GUI 中嵌入 Matplotlib 时，您必须直接使用 Matplotlib API，而不是 pylab/pyplot 过程接口，因此请查看 examples/api 目录以获取一些与 API 一起工作的示例代码。

```{toctree}
embedding-in-qt
embedding-in-tk
svg-histogram
svg-tooltip
toolmanager
wxcursor
tk-images
```
