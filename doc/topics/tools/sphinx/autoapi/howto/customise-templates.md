# 如何通过模板定制布局

您可以通过更改 AutoAPI 使用的 `Jinja2` 模板来定制它生成的文档的外观。默认模板位于 `autoapi` 包的 `autoapi/templates` 目录中。只需将您想要自定义的模板复制到本地目录并编辑它们。要让 AutoAPI 使用这些模板，请将 [`autoapi_template_dir`](https://sphinx-autoapi.readthedocs.io/en/latest/reference/config.html#confval-autoapi_template_dir) 配置选项指向您的目录。它可以是绝对的，也可以是相对于文档源目录的根目录(即传递给 `sphinx-build` 的目录)。

```python
autoapi_template_dir = '_autoapi_templates'
```

模板目录必须遵循与默认模板相同的布局。例如，要覆盖 Python 类和模块模板：

```
_autoapi_templates
└── python
    ├── class.rst
    └── module.rst
```
