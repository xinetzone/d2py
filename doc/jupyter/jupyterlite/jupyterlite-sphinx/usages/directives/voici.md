# Voici directive

`jupyterlite-sphinx` 提供了 `voici` 指令，允许你在文档中嵌入 [voici仪表板](https://github.com/voila-dashboards/voici)。

```rst
.. voici::
   :height: 600px
```

```{eval-rst}
.. voici::
   :height: 600px
```

可以提供将使用 Voici 呈现的笔记本：

```rst
.. voici:: my_notebook.ipynb
   :height: 600px
   :prompt: Try Voici!
   :prompt_color: #dc3545
```

```{eval-rst}
.. voici:: my_notebook.ipynb
   :height: 600px
   :prompt: Try Voici!
   :prompt_color: #dc3545
```
