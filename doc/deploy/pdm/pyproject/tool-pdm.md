# PDM 工具设置

还有一些有用的设置来控制 PDM 的打包行为。它们应该与 `pyproject.toml` 一起运送，在 `[tool.pdm]` 表中定义。

## 开发依赖性

你可以有几组仅供开发的依赖关系。与 `optional-dependencies` 不同，它们不会出现在软件包的元数据中，如 `PKG-INFO` 或 `METADATA`。而且包的索引也不会知道这些依赖关系。这个模式与 `optional-dependencies` 类似，只是它在 `tool.pdm` 表中。

```toml
[tool.pdm.dev-dependencies]
lint = [
    "flake8",
    "black"
]
test = ["pytest", "pytest-cov"]
doc = ["mkdocs"]
```

要安装所有这些东西：

```bash
pdm install
```

更多的 CLI 使用方法，请参考 [管理依赖性](../usage/dependency/)。

`dev-dependencies` 中也允许编辑依赖项。定义可编辑的依赖，用 `-e ` 前缀：

```toml
[tool.pdm.dev-dependencies]
editable = [
    "-e git+https://github.com/pallets/click.git@main#egg=click",  # VCS link
    "-e ./mypackage/",  # local package
]
```

## 在解析结果中允许预发布

默认情况下，`pdm` 的依赖项解析器将忽略预发布版本，除非在给定的依赖项版本范围内没有稳定的版本。这种行为可以通过在 `[tool.pdm]` 中设置 `allow_prereleases` 为 `true` 来改变：

```toml
[tool.pdm]
allow_prereleases = true
```

## 指定其他寻找软件包的来源

像 Pipenv 一样，你可以指定额外的来源来寻找具有相同格式的软件包。它们被存储在 `pyproject.toml` 中名为 `[[tool.pdm.source]]` 的数组表中：

```toml
[[tool.pdm.source]]
url = "https://private-site.org/pypi/simple"
verify_ssl = true
name = "internal"
```

这样，就可以在 PyPI 索引和上面的内部源中搜索包。这就像 `--extra-index-url https://private-site.org/pypi/simple` 被传递给 `pip install` 一样。

### 禁用 PyPI 存储库

如果你想忽略默认的 PyPI 索引，只需将源名称设置为 `pypi`，该源将 **替换** 它。

```toml
[[tool.pdm.source]]
url = "https://private.pypi.org/simple"
verify_ssl = true
name = "pypi"
```

### 查找链接源

By default, all sources are PEP 503 style "indexes" like pip's --index-url and --extra-index-url, however, you can also specify "find links" with type = "find_links". See this answer for the difference between the two types.

默认情况下，或来源是 {pep}`503` 风格的 "索引"，就像 `pip` 的 `--index-url` 和 `--extra-index-url`，然而，你也可以用 `type = "find_links"` 指定 "查找链接"。关于这两种类型的区别，见 [回答](https://stackoverflow.com/a/46651848)。

例如，从包含包文件的本地目录安装：

```toml
[[tool.pdm.source]]
url = "file:///path/to/packages"
name = "local"
type = "find_links"
```

```{admonition} 改变配置值的差异
当你想从给定的索引中获取所有的软件包，而不是默认的索引，尽管你在什么平台上或者谁来部署应用程序。写在 `[[tool.pdm.source]]` 里。否则，如果你想在当前平台上临时改变索引（出于网络原因），你应该使用 `pdm config pypi.url https://private.pypi.org/simple`。
```

### 遵循资料来源的顺序

默认情况下，所有来源的包被认为是相等的，来自它们的包按照版本和 wheel tags 进行排序，选择与最高版本匹配度最高的包。

在某些情况下，您可能希望从首选源返回包，并搜索从前一个源中丢失的其他包。PDM 通过读取配置 `respect-source-order` 来支持这一点：

```toml
[tool.pdm.resolution]
respect-source-order = true
```
