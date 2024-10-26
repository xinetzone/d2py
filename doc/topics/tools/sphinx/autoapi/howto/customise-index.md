# 如何自定义索引页

AutoAPI 创建的索引页是使用模板生成的。因此，定制索引页的步骤与定制模板的步骤相同。只需编辑 `autoapi/templates/index`。使用与[自定义模板](customise-templates)相同的步骤创建 RST 模板。

## 如何删除索引页

要完全删除索引页，请关闭 [`autoapi_add_toctree_entry`](https://sphinx-autoapi.readthedocs.io/en/latest/reference/config.html#confval-autoapi_add_toctree_entry) 配置选项：

```python
autoapi_add_toctree_entry = False
```

然后，您需要自己将生成的文档包含在 `toctree` 中。例如，如果你正在为名为 “example” 的包生成文档，你将添加以下 `toctree` 条目：

```rst
.. toctree::

    autoapi/example/index
```

注意，`autoapi/` 是文档的默认位置，由 [`autoapi_root`](https://sphinx-autoapi.readthedocs.io/en/latest/reference/config.html#confval-autoapi_root) 配置。如果您更改了 `autoapi_root`，那么您需要添加的条目也会更改。

## 如何配置文档出现在 TOC 树中的位置

`autoapi_root` 配置选项定义在何处输出生成的文档。要更改文档的输出位置，只需将此选项更改为相对于文档源目录的另一个目录：

```
autoapi_root = 'technical/api'
```
