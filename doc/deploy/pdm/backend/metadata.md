# 项目元数据

项目元数据存储在基于 {pep}`621` 的 `pyproject.toml` 的 `project` 表中。除此之外，还支持一些额外的特性。

## 动态项目版本

`pdm-backend` 可以动态地确定项目的版本。要做到这一点，你需要从 `pyproject.toml` 中去掉 `version` 字段，并将 `version` 添加到 `project.dynamic` 列表中：

```
[project]
...
- version = "0.1.0" remove this line
+ dynamic = ["version"]
```

然后在 `[tool.pdm.version]` 表中指定如何获取版本信息。支持三种方式：

```{rubric} 从给定文件路径中的静态字符串中读：
```

```toml
[tool.pdm.version]
source = "file"
path = "mypackage/__init__.py"
```

这样，文件必须包含如下一行：

```python
__version__ = "0.1.0" # Single quotes and double quotes are both OK, comments are allowed.
```

```{rubric} 从 SCM 标签读取，支持 git 和 hg
```

```toml
[tool.pdm.version]
source = "scm"
```

当从 SCM 不可用的源代码树构建时，可以使用环境变量 `PDM_BUILD_SCM_VERSION` 来假装设置了版本：

```bash
PDM_BUILD_SCM_VERSION=0.1.0 python -m build
```

```{rubric} 得到特定的函数
```

```toml
[tool.pdm.version]
source = "call"
getter = "mypackage.version.get_version"
```

也可以为它提供字面参数：

```toml
getter = "mypackage.version.get_version('dev')"
```

## 写入动态版本文件

您可以指示 `pdm-backend` 将动态版本回写到文件中。除了 `file`，所有源码都支持它。

```toml
[tool.pdm.version]
source = "scm"
write_to = "foo/version.txt"
```

默认情况下，`pdm-backend` 只编写 SCM 版本本身。可以将模板作为 Python 格式的字符串提供，以创建语法正确的 Python 赋值：

```python
[tool.pdm.version]
source = "scm"
write_to = "foo/_version.py"
write_template = "__version__ = '{}'"
```

```{note}
`pdm-backend` 每次都会重写整个文件，因此不能在该文件中添加其他内容。
```

## 变量拓展

### 环境变量

你可以在依赖项字符串中以 `${VAR}` 的形式引用环境变量，两者都适用于 `dependencies` 和 `optional-dependencies`：

```toml
[project]
dependencies = [
    "foo @ https://${USERNAME}:${PASSWORD}/mypypi.org/packages/foo-0.1.0-py3-none-any.whl"
]
```

在构建项目时，变量将使用环境变量的当前值展开。

### 相对路径

您可以使用相对路径向项目根添加依赖项。要做到这一点，`pdm-backend` 提供了特殊的变量 `${PROJECT_ROOT}` 来引用项目根，并且依赖关系必须用 `file://` 定义：

```toml
[project]
dependencies = [
    "foo @ file:///${PROJECT_ROOT}/foo-0.1.0-py3-none-any.whl"
]
```

引用项目根目录以外的包：

```toml
[project]
dependencies = [
    "foo @ file:///${PROJECT_ROOT}/../packages/foo-0.1.0-py3-none-any.whl"
]
```

```{note}
三个斜杠 `///` 是 Windows 和 POSIX 系统兼容性所必需的。

相对路径将扩展为本地机器上的绝对路径。因此，在发行版中包含它们是没有意义的，因为其他安装包的人不会有相同的路径。
```
