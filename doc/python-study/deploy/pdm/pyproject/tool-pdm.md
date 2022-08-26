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

## 指定其他寻找软件包的来源

像 Pipenv 一样，你可以指定额外的来源来寻找具有相同格式的软件包。它们被存储在 `pyproject.toml` 中名为 `[[tool.pdm.source]]` 的数组表中：

```toml
[[tool.pdm.source]]
url = "https://private-site.org/pypi/simple"
verify_ssl = true
name = "internal"
```

这就像 `--extra-index-url https://private-site.org/pypi/simple` 被传递一样。

或者你可以通过使用一个名为 `pypi` 的源来覆盖 `pypi.url` 值：

```toml
[[tool.pdm.source]]
url = "https://private.pypi.org/simple"
verify_ssl = true
name = "pypi"
```

默认情况下，或来源是 {pep}`503` 风格的 "索引尿"，就像管道的 `--index-url` 和 `--extra-url`，然而，你也可以用 `type = "find_links"` 指定 "查找链接"。关于这两种类型的区别，见 [回答](https://stackoverflow.com/a/46651848)。

```{admonition} 改变配置值的差异
当你想从给定的索引中获取所有的软件包，而不是默认的索引，尽管你在什么平台上或者谁来部署应用程序。写在 `[[tool.pdm.source]]` 里。否则，如果你想在当前平台上临时改变索引（出于网络原因），你应该使用 `pdm config pypi.url https://private.pypi.org/simple`。
```

## 包含和排除软件包文件

指定包括和排除文件的方法很简单，它们是以 glob 模式的列表形式给出的：

```toml
includes = [
    "**/*.json",
    "mypackage/",
]
excludes = [
    "mypackage/_temp/*"
]
```

如果你希望某些文件只包含在 sdist 中，你可以使用 `source-includes` 字段。

```toml
includes = [...]
excludes = [...]
source-includes = ["tests/"]
```

注意，在 `source-includes` 中定义的文件将在非 dist 构建中自动排除。

### 包括和排除的默认值

如果你没有指定任何这些字段，PDM 也提供智能默认值，以适应最常见的工作流程。

- 顶级包将被包括在内。
- `tests` 包将被排除在 **非 sdist** 的构建之外。
- `src` 目录将被检测为 `package-dir`，如果它存在的话。

如果你的项目遵循上述惯例，你不需要配置任何这些字段，它就能工作。请注意 PDM 不会自动添加 {pep}`PEP 420 隐式命名空间包 <420>`，它们应该总是在 `includes` 中明确指定。

## 选择另一个软件包目录来寻找软件包

与 `setuptools` 的 `package_dir` 设置类似，人们可以在 `pyproject.toml` 中轻松指定另一个软件包目录，如 `src`。

```toml
package-dir = "src"
```

如果没有给出软件包目录，PDM 也可以识别 `src` 作为 `package-dir` ，如果：

1. `src/__init__.py` 不存在，意味着它不是一个有效的 Python 包，并且
2. `src/*` 下存在一些软件包。

## 隐式命名空间包

正如 {pep}`420` 中规定的那样，如果一个目录被确认为一个命名空间包，那么：

1. `<package>/__init__.py` 不存在，并且
2. 在 `<package>/*` 下存在正常的包和/或其他命名空间的包，并且
3. `<package>` 被明确地列在了 `includes` 中

## 构建 C 语言扩展

目前，构建 C 语言扩展仍然依赖于 `setuptools`。你应该写一个 python 脚本，其中包含一个名为 `build` 的函数，并接受 `setup()` 的参数字典作为唯一参数。在函数中用你的 `ext_modules` 设置更新字典。

下面是一个取自 `MarkupSafe` 的例子：

```python
# build.py
from setuptools import Extension

ext_modules = [Extension("markupsafe._speedups", ["src/markupsafe/_speedups.c"])]

def build(setup_kwargs):
    setup_kwargs.update(ext_modules=ext_modules)
```

现在，通过 `pyproject.toml` 中的 `build` 指定构建脚本路径：

```toml
# pyproject.toml
[tool.pdm]
build = "build.py"
```

默认情况下，每次构建都是在一个干净和隔离的环境中进行，只有构建需求可以被看到。如果你的构建有依赖项目环境的可选需求，你可以通过 `pdm build --no-isolation` 关闭环境隔离，或者将配置 `build_isolation` 设置为假值。

## 可编辑的构建后端

PDM 利用 {pep}`660` 来建立可编辑安装的轮子。人们可以从这两种方法中选择如何生成轮子：

- `editables`：（默认）在软件包路径下创建代理模块。
- `path`：setuptools 使用的传统方法，在软件包路径下创建 .pth 文件。 

请阅读 PEP，了解这两种方法的区别以及它们的工作原理。

在 `pyproject.toml` 中指定该方法，如下所示：

```toml
[tool.pdm]
editable-backend = "path"
```

`editables` 后端更值得推荐，但有一个已知的限制，即它不能与 {pep}`420` 命名空间包一起工作。所以在这种情况下，你需要改成 `path`。


```{admonition} 关于 Python 2 的兼容性
由于 PDM 管理的项目的构建后端需要 Python>=3.6，如果 Python 2 被用作主机解释器，你将不能安装当前项目。你仍然可以安装其他没有 PDM 支持的依赖项。
```
