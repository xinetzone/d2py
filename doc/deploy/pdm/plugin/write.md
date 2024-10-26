# 编写 PDM 插件

PDM 的目标是成为社区驱动的软件包管理器。它配备了全功能的插件系统，你可以用它：

- 为 PDM 开发新的命令
- 为现有的 PDM 命令添加额外的选项
- 通过读取额外的配置项来改变 PDM 的行为
- 控制依赖关系的解决或安装过程

## PDM 插件应该做什么

核心的 PDM 项目专注于依赖性管理和包的发布。你希望与 PDM 集成的其他功能，最好放在自己的插件中并作为独立的 PyPI 项目发布。如果该插件被认为是核心项目的一个很好的补充，它可能有机会被吸收到 PDM 中。

## 编写你自己的 PDM 插件

在下面的章节中，将展示添加新命令 `hello` 的例子，它读取 `hello.name` 的配置。

### 编写 PDM 命令

PDM 的 CLI 模块的设计方式是，用户可以很容易地 "继承和修改"。要编写新的命令：

```python
import argparse
from pdm.project import Project
from pdm.cli.commands.base import BaseCommand

class HelloCommand(BaseCommand):
    """向指定的人问好。
    如果没有给出，将从 "hello.name" 配置中读取。
    """

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument("-n", "--name", 
                            help="the person's name to whom you greet")

    def handle(self, project: Project, options: argparse.Namespace):
        if not options.name:
            name = project.config["hello.name"]
        else:
            name = options.name
        print(f"Hello, {name}")
```

首先，创建新的 `HelloCommand` 类，继承自 {class}`pdm.cli.command.base.BaseCommand`。它有两个主要功能：

- {meth}`add_arguments` 来操作作为唯一参数传递的参数解析器。在这里你可以向它添加额外的命令行参数。
- {meth}`handle` 在子命令被匹配时做一些事情，你可以通过写 `pass` 语句来做任何事情。它接受两个参数：第一个是 {class}`pdm.project.Project` 对象，第二个是解析后的 {class}`argparse.Namespace` 对象。

该文件字符串将作为命令帮助文本，在 `pdm --help` 中显示。

此外，PDM 的子命令有两个默认选项：`-v/--verbose` 用于改变 verbosity 程度，`-g/--global` 用于启用全局项目。如果你不想要这些默认选项，可以将 `arguments` 类属性覆盖到 `pdm.cli.options.Option` 对象的列表中，或者将其分配到一个空列表中，就没有默认选项了：

```python hl_lines="3"
class HelloCommand(BaseCommand):

    arguments = []
```

```{note}
首先加载默认选项，然后调用 `add_arguments()`。
```
    
### 将命令注册到 PDM 核心对象

在你的插件项目的某个地方写一个函数。对函数的名称没有限制。但该函数应该只接受一个参数 -- PDM 核心对象：

```python hl_lines="2"
def hello_plugin(core):
    core.register_command(HelloCommand, "hello")
```

调用 `core.register_command()` 来注册该命令。第二个参数作为子命令的名称是可选的。如果没有传递名称，PDM 将寻找 `HelloCommand` 的 `name` 属性。

### 添加新的 PDM 配置项

回顾第一个代码片断，如果不是通过命令行传递，`hello.name` 配置键会被查询到名字。

```{eval-rst}
.. code-block:: python
    :linenos:
    :emphasize-lines: 16

    import argparse
    from pdm.project import Project
    from pdm.cli.commands.base import BaseCommand

    class HelloCommand(BaseCommand):
        """向指定的人问好。
        如果没有给出，将从 "hello.name" 配置中读取。
        """

        def add_arguments(self, parser: argparse.ArgumentParser):
            parser.add_argument("-n", "--name", 
                                help="the person's name to whom you greet")

        def handle(self, project: Project, options: argparse.Namespace):
            if not options.name:
                name = project.config["hello.name"]
            else:
                name = options.name
            print(f"Hello, {name}")
```

到现在为止，如果你通过 `pdm config get hello.name` 查询配置值，会弹出错误，说它不是有效的配置键。你也需要注册这个配置项：

```{eval-rst}
.. code-block:: python
    :linenos:
    :emphasize-lines: 5

    from pdm.project.config import ConfigItem

    def hello_plugin(core):
        core.register_command(HelloCommand, "hello")
        core.add_config("hello.name", ConfigItem("The person's name", "John"))
```

其中 `ConfigItem` 类需要 4 个参数，顺序如下：

- `description`：对配置项的描述
- `default`：配置项的默认值 
- `global_only`：是否只允许在主配置中设置配置
- `env_var`：环境变量的名称，将作为配置值被读取

### PDM 其他插件点

除了命令和配置，"核心" 对象还暴露了一些其他的方法和属性来覆盖。PDM 还提供了一些你可以监听的信号。请阅读 [API参考](https://pdm.fming.dev/plugin/reference/) 了解更多细节。

### 关于开发 PDM 插件的提示

在开发插件时，人们希望在开发中激活和插件，并在代码改变时得到更新。这通常是通过 `pip install -e .` 或 `python setup.py develop` 在传统的 Python 包装世界中，利用 `setup.py` 来实现。然而。由于在 PDM 项目中没有这样的 `setup.py`，我们如何才能做到呢？

幸运的是，有了 PDM 和 {pep}`582`，它变得更加容易。首先，你应该在全局范围内启用 {pep}`582`。然后你只需要通过以下方式将所有的依赖项安装到 `__pypackages__` 目录中：

```bash
pdm install
```

之后，所有的依赖都可以用兼容的 Python 解释器，包括插件本身，在可编辑模式下。这意味着对代码库的任何改变都会立即生效，而不需要重新安装。`pdm` 可执行文件也在引擎盖下使用 Python 解释器。所以如果你在插件项目中运行 `pdm`，开发中的插件将被自动激活，你可以做一些测试，看看它是如何工作的。这就是  {pep}`582` 对开发工作流程的好处。

### 测试 PDM 插件


在 [pdm.pytest](https://pdm.fming.dev/dev/plugin/fixtures/) 模块中 PDM 中将一些 pytest fixture 作为插件公开。要从中受益，必须将 `pdm[pytest]` 添加为测试依赖项。

要在测试中启用它们，请添加 `pdm.pytest` 作为插件。你可以在你的根目录 `conftest.py` 中这样做：

```{eval-rst}
.. code-block:: python
    :linenos:
    :caption: conftest.py

    # single plugin
    pytest_plugins = "pytest.plugin"

    # many plugins
    pytest_plugins = [
        ...
        "pdm.pytest",
        ...
    ]
```

可以在 PDM 自己的 [tests](https://github.com/pdm-project/pdm/tree/main/tests) 中看到一些使用示例，特别是用于配置的 [`conftest.py`](https://github.com/pdm-project/pdm/blob/main/tests/conftest.py) 文件。

## 发布 PDM 插件

现在定义了你的插件，把它分发到 PyPI。PDM 的插件是通过入口点类型发现的。创建 `pdm` 入口点，并指向你的插件可调用（是的，它不需要是函数，任何可调用对象都可以）：

**PEP 621**:

```toml
# pyproject.toml

[project.entry-points.pdm]
hello = "my_plugin:hello_plugin"
```

**setuptools**:

```python
# setup.py

setup(
    ...
    entry_points={"pdm": ["hello = my_plugin:hello_plugin"]}
    ...
)
```

## 激活 PDM 插件

由于插件是通过入口点加载的，它们可以在没有更多步骤的情况下被激活，而只是安装插件。为了方便，PDM 提供了一个 `plugin` 命令组来管理插件。

假设你的插件是以 `pdm-hello` 的名义发布的：

```bash
pdm plugin add pdm-hello
```

现在在终端输入 `pdm --help`，你会看到新增加的 `hello` 命令并使用它：

```bash
$ pdm hello Jack
Hello, Jack
```

通过在终端键入 `pdm plugin --help` 查看更多插件管理子命令。
