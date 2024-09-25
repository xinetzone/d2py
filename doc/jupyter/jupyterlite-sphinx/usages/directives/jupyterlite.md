# JupyterLite 指令

`jupyterlite-sphinx` 提供了 `jupyterlite` 指令，允许你在文档中嵌入 JupyterLab。

```rst
.. jupyterlite::
   :width: 100%
   :height: 600px
   :prompt: Try JupyterLite!
   :prompt_color: #00aa42
```

```{eval-rst}
.. jupyterlite::
   :width: 100%
   :height: 600px
   :prompt: Try JupyterLite!
   :prompt_color: #00aa42
```

你也可以通过传递 Notebook 文件来自动打开它。

```rst
.. jupyterlite:: my_notebook.ipynb
   :width: 100%
   :height: 600px
   :prompt: Try JupyterLite!
   :prompt_color: #00aa42
```

```{eval-rst}
.. jupyterlite:: my_notebook.ipynb
   :width: 100%
   :height: 600px
   :prompt: Try JupyterLite!
   :prompt_color: #00aa42
```

`search_params` 指令允许将一些搜索参数从文档URL传递到 Jupyterlite URL。然后，Jupyterlite 将从其自己的 URL 中获取这些参数。例如，`:search_params: ["param1", "param2"]`将传输参数*param1*和*param2*。使用布尔值来传输所有或无参数（默认为 `none`）：`:search_params: True`

