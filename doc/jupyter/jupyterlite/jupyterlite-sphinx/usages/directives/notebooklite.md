# NotebookLite 指令

`jupyterlite-sphinx` 提供了 `notebooklite` 指令，允许你在文档中嵌入经典的Notebook UI。

```rst
.. notebooklite::
   :width: 100%
   :height: 600px
   :prompt: Try classic Notebook!
```

```{eval-rst}
.. notebooklite::
   :width: 100%
   :height: 600px
   :prompt: Try classic Notebook!
```

你也可以通过传递 Notebook 文件来打开它：

```rst
.. notebooklite:: my_notebook.ipynb
   :width: 100%
   :height: 600px
   :prompt: Try classic Notebook!
```

```{eval-rst}
.. notebooklite:: my_notebook.ipynb
   :width: 100%
   :height: 600px
   :prompt: Try classic Notebook!
```
