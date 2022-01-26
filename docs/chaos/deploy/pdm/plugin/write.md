# 编写插件

PDM 的目标是成为一个社区驱动的软件包管理器。它配备了一个全功能的插件系统，你可以用它：

- 为 PDM 开发新的命令
- 为现有的 PDM 命令添加额外的选项
- 通过读取额外的配置项来改变 PDM 的行为
- 控制依赖关系的解决或安装过程

## 插件应该做什么

核心的 PDM 项目专注于依赖性管理和包的发布。你希望与 PDM 集成的其他功能，最好放在自己的插件中并作为独立的 PyPI 项目发布。如果该插件被认为是核心项目的一个很好的补充，它可能有机会被吸收到 PDM 中。

## 编写你自己的插件

在下面的章节中，我将展示一个添加新命令 `hello` 的例子，它读取 `hello.name` 的配置。

### 编写命令

PDM 的 CLI 模块的设计方式是，用户可以很容易地 "继承和修改"。要编写新的命令：

```python
from pdm.cli.commands.base import BaseCommand

class HelloCommand(BaseCommand):
    """Say hello to the specified person.
    If none is given, will read from "hello.name" config.
    """

    def add_arguments(self, parser):
        parser.add_argument("-n", "--name", help="the person's name to whom you greet")

    def handle(self, project, options):
        if not options.name:
            name = project.config["hello.name"]
        else:
            name = options.name
        print(f"Hello, {name}")
```

首先，让我们创建一个新的 `HelloCommand` 类，继承自 `pdm.cli.command.base.BaseCommand`。它有两个主要功能：

- `add_arguments()` 来操作作为唯一参数传递的参数解析器。在这里你可以向它添加额外的命令行参数
- `handle()` 在子命令被匹配时做一些事情，你可以通过写一个 `pass` 语句来做任何事情。它接受两个参数：第一个是 `pdm.project.Project` 对象，第二个是解析后的 `argparse.Namespace` 对象。

该文件字符串将作为命令帮助文本，在 `pdm --help` 中显示。

此外，PDM 的子命令有两个默认选项：`-v/--verbose` 用于改变 verbosity 程度，`-g/--global` 用于启用全局项目。如果你不想要这些默认选项，可以将 `arguments` 类属性覆盖到 `pdm.cli.options.Option` 对象的列表中，或者将其分配到一个空列表中，就没有默认选项了：

```python hl_lines="3"
class HelloCommand(BaseCommand):

    arguments = []
```

```{note}
首先加载默认选项，然后调用 `add_arguments()`。
```
    
### 将命令注册到核心对象

在你的插件项目的某个地方写一个函数。对函数的名称没有限制。但该函数应该只接受一个参数 -- PDM 核心对象：

```python hl_lines="2"
def hello_plugin(core):
    core.register_command(HelloCommand, "hello")
```

调用 `core.register_command()` 来注册该命令。第二个参数作为子命令的名称是可选的。如果没有传递名称，PDM 将寻找 `HelloCommand` 的 `name` 属性。

### 添加新的配置项

让我们回顾一下第一个代码片断，如果不是通过命令行传递，`hello.name` 配置键会被查询到名字。

```python hl_lines="11"
class HelloCommand(BaseCommand):
    """Say hello to the specified person.
    If none is given, will read from "hello.name" config.
    """

    def add_arguments(self, parser):
        parser.add_argument("-n", "--name", help="the person's name to whom you greet")

    def handle(self, project, options):
        if not options.name:
            name = project.config["hello.name"]
        else:
            name = options.name
        print(f"Hello, {name}")
```

到现在为止，如果你通过 `pdm config get hello.name` 查询配置值，会弹出一个错误，说它不是一个有效的配置键。你也需要注册这个配置项：

```python hl_lines="5"
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

### 其他插件点

除了命令和配置，"核心" 对象还暴露了一些其他的方法和属性来覆盖。PDM 还提供了一些你可以监听的信号。请阅读 [API参考](https://pdm.fming.dev/plugin/reference/) 了解更多细节。

### 关于开发 PDM 插件的提示

在开发插件时，人们希望在开发中激活和插件，并在代码改变时得到更新。这通常是通过 `pip install -e .` 或 `python setup.py develop` 在传统的 Python 包装世界中，利用 `setup.py` 来实现。然而。由于在 PDM 项目中没有这样的 `setup.py`，我们如何才能做到呢？

幸运的是，有了 PDM 和 PEP 582，它变得更加容易。首先，你应该在全局范围内启用 {pep}`582`，按照 [本文档的相应部分](../index.md#enable-pep-582-globally)。然后你只需要通过以下方式将所有的依赖项安装到 `__pypackages__` 目录中：

```bash
pdm install
```

之后，所有的依赖都可以用兼容的 Python 解释器，包括插件本身，在可编辑模式下。这意味着对代码库的任何改变都会立即生效，而不需要重新安装。`pdm` 可执行文件也在引擎盖下使用 Python 解释器。所以如果你在插件项目中运行 `pdm`，开发中的插件将被自动激活，你可以做一些测试，看看它是如何工作的。这就是 PEP 582 对我们开发工作流程的好处。

## 发布插件

现在你已经定义了你的插件，让我们把它分发到 PyPI。PDM 的插件是通过入口点类型发现的。创建一个 `pdm` 入口点，并指向你的插件可调用（是的，它不需要是一个函数，任何可调用对象都可以）：

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

## 激活插件

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
