# 构建配置

`pdm` 使用 {pep}`517` 来构建包。构建后端驱动构建系统从任意源树构建源分布和轮子。

`pdm` 还附带了自己的构建后端 [`pdm-pep517`](https://pypi.org/project/pdm-pep517/)。除了 [PEP 621项目元数据](pep621)，它还读取存储在 `[tool.pdm.build]` 中的其他配置来控制构建行为。要使用它，请在 `pyproject.toml` 中包含以下内容（如果您使用 `pdm init` 或 `pdm import` 来创建文件，它将自动完成）：

```toml
[build-system]
requires = ["pdm-pep517"]
build-backend = "pdm.pep517.api"
```

```{note}
本文档的以下部分假设您使用的是上面提到的 `pdm-pep517` 后端。不同的后端会有不同的配置。
```

(pdm:dynamic-versioning)=
## 动态版本

`pdm-pep517` 支持两个源码的动态版本。要启用动态版本控制，请记住在 PEP 621 元数据的 `dynamic` 字段中包含 `version`：

```toml
[project]
...
dynamic = ["version"]
```

### 来自文件的动态版本

```toml
[tool.pdm]
version = { source = "file", path = "mypackage/__version__.py" }
```

后端将在给定文件中搜索模式 `__version__ = "{version}"`，并使用该值作为版本。

````{tip}
多亏了 TOML 语法，上面的例子等价于以下内容：

```toml
[tool.pdm.version]
source = "file"
path = "mypackage/__version__.py"
```
或者
```toml
[tool.pdm]
version.source = "file"
version.path = "mypackage/__version__.py"
```
````

### 来自 SCM 的动态版本

如果您使用过 [`setuptools-scm`](https://pypi.org/project/setuptools-scm/)，就会熟悉这种方法。`pdm-pep517` 还可以从 SCM 存储库的标记中读取版本：

```toml
[tool.pdm]
version = { source = "scm" }
```

#### 手动指定版本

在构建包时，`pdm-pep517` 将要求 SCM 可用来填充版本。如果不是这样，您仍然可以使用环境变量 `PDM_PEP517_SCM_VERSION` 指定版本：

```bash
export PDM_PEP517_SCM_VERSION="1.2.3"
pdm build
```

#### 将版本写入文件

对于从 SCM 读取的动态版本，在构建轮子时将评估值写入文件将很有帮助，这样您就不需要 `importlib.metadata` 来获取代码中的版本。

```toml
[tool.pdm.version]
source = "scm"
write_to = "mypackage/__version__.py"
write_template = "__version__ = '{}'"  # optional, default to "{}"
```

对于源代码发行版，版本将被 **冻结** 并转换为 `pyproject.toml` 文件中的静态版本，它将包含在发行版中。

## 包含和排除文件

指定包括和排除文件的方法很简单，它们是以 glob 模式的列表形式给出的：

```toml
[tool.pdm.build]
includes = [
    "**/*.json",
    "mypackage/",
]
excludes = [
    "mypackage/_temp/*"
]
```

```{note}
当使用 `includes` 时，默认的 `includes` 将被覆盖。您必须手动添加包路径。
```

如果你希望某些文件只包含在 sdist 中，你可以使用 `source-includes` 字段。

```
[tool.pdm.build]
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
[tool.pdm.build]
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

## 自定义文件生成

在构建过程中，您可能希望生成其他文件或从 internet 下载资源。你可以通过 `setup-script` 构建配置来实现：

```toml
[tool.pdm.build]
setup-script = "build.py"
```

在 `build.py` 脚本中，`pdm-pep517` 查找 `build` 函数并使用两个参数调用它：

- `src`: (str) 源目录的路径
- `dst`: (str) 分发目录的路径

示例：

```python
# build.py
def build(src, dst):
    target_file = os.path.join(dst, "mypackage/myfile.txt")
    os.makedirs(os.path.dirname(target_file), exist_ok=True)
    download_file_to(dst)
```

生成的文件将被复制到具有相同层次结构的结果轮子中，如果需要，您需要创建父目录。

## 构建平台特定的轮子

`setup-script` 也可以用来构建特定于平台的轮子，比如 C 扩展。目前，构建 C 扩展仍然依赖于 `setuptools`。

在 `setup-script` 下设置  `run-setuptools = true`，`pdm-pep517` 将生成 `setup.py`，其中包含脚本中的自定义 `build` 函数，然后运行  `python setup.py build` 来构建轮子和任何扩展：

```toml
# pyproject.toml
[tool.pdm.build]
setup-script = "build_setuptools.py"
run-setuptools = true
```

在 `setup-script` 本中，预期的 `build` 函数接收要传递给 `setuptools.setup()` 调用的参数字典。在函数中，您可以根据需要使用任何附加值或更改值更新[关键字字典](https://setuptools.pypa.io/en/latest/references/keywords.html)。

下面是取自 `MarkupSafe` 的例子：

```python
# build_setuptools.py
from setuptools import Extension

ext_modules = [
    Extension("markupsafe._speedups", ["src/markupsafe/_speedups.c"])
]

def build(setup_kwargs):
    setup_kwargs.update(ext_modules=ext_modules)
```

如果您运行 `pdm build` （或任何其他构建前端，如 [build](https://pypi.org/project/build)）， `pdm` 将构建特定于平台的轮子文件以及 sdist。

默认情况下，每次构建都是在一个干净和隔离的环境中进行，只有构建需求可以被看到。如果你的构建有依赖项目环境的可选需求，你可以通过 `pdm build --no-isolation` 关闭环境隔离，或者将配置 `build_isolation` 设置为假值。

## 重写 "Is-Purelib" 值

如果未指定此值，如果 `run-setuptools` 为 `true`，`pdm-pep517` 将构建特定于平台的轮子。

有时您可能希望构建特定于平台的轮子，但没有构建脚本（二进制文件可能由其他工具构建或获取）。在这种情况下，你可以在 `pyproject.toml` 中设置 `is-purelib` 值为 `false`：

```toml
[tool.pdm.build]
is-purelib = false
```

## 可编辑的构建后端

PDM 利用 {pep}`660` 来建立可编辑安装的轮子。人们可以从这两种方法中选择如何生成轮子：

- `path`（默认）：setuptools 使用的传统方法，在软件包路径下创建 `.pth` 文件。 
- `editables`: 在软件包路径下创建代理模块。由于代理模块是在运行时查找的，因此它可能无法与某些静态分析工具一起工作。

请阅读 PEP，了解这两种方法的区别以及它们的工作原理。

在 `pyproject.toml` 中指定该方法，如下所示：

```toml
[tool.pdm.build]
editable-backend = "path"
```

`editables` 后端更值得推荐，但有一个已知的限制，即它不能与 {pep}`420` 命名空间包一起工作。所以在这种情况下，你需要改成 `path`。


```{admonition} 关于 Python 2 的兼容性
由于 PDM 管理的项目的构建后端需要 Python>=3.6，如果 Python 2 被用作主机解释器，你将不能安装当前项目。你仍然可以安装其他没有 PDM 支持的依赖项。
```

## 使用其他 PEP 517 后端

除了 `pdm-pep517` 之外，`pdm` 还可以与任何读取 PEP 621 元数据的 PEP 517 构建后端一起使用。在撰写本文时，[`flit`](https://pypi.org/project/flit)（后端 `flit-core`）和 [`hatch`](https://pypi.org/project/hatch)（后端 `hatchling`）与 PEP 621 一起工作得很好，[`setuptools`](https://pypi.org/project/setuptools) 有实验支持。要使用其中一个，你可以在 `pyproject.toml` 中指定后端：

```toml
[build-system]
requires = ["flit_core >=3.2,<4"]
build-backend = "flit_core.buildapi"
```

当执行 `pdm build` 时，PDM 将调用正确的后端。
