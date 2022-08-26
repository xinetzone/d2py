# 管理项目

PDM 可以作为 {pep}`517` 的构建后端，要启用它，请在你的 `pyproject.toml`。如果你用 `pdm init` 为你创建它，应该已经完成了。

```toml
[build-system]
requires = ["pdm-pep517"]
build-backend = "pdm.pep517.api"
```

`pip` 将读取后台设置来安装或构建软件包。

## 选择 Python 解释器

如果你使用过 `pdm init`，你一定已经看到了 PDM 是如何检测和选择 Python 解释器。在初始化之后，你也可以通过 `pdm use <python_version_or_path>` 来改变设置。参数可以是任何长度的版本说明，也可以是相对或绝对的路径，指向相对或绝对路径，但请记住，Python 解释器必须符合项目文件中的 `python_requires` 的约束。的约束。

### `requires-python` 如何控制项目

PDM 尊重 `requires-python` 的价值，它试图挑选能够在 `requires-python` 包含的所有 python 版本上工作的候选包。在所有 `requires-python` 包含的 python 版本上工作。例如，如果 `requires-python` 是 `>=2.7`，PDM 将尝试找到最新版本的 `foo`，其 `requires-python` 的版本范围是 `>=2.7` 的 **superset**。

因此，如果你不希望任何过时的软件包被锁定，请确保你正确地编写 `requires-python`。

## 构建分发工件

```console
$ pdm build
- Building sdist...
- Built pdm-test-0.0.0.tar.gz
- Building wheel...
- Built pdm_test-0.0.0-py3-none-any.whl
```

然后可以通过 [twine](https://pypi.org/project/twine) 或使用 [pdm-publish](https://github.com/branchvincent/pdm-publish) 插件将工件上传至 PyPI。可用的选项可以通过输入 `pdm build --help` 即可找到可用的选项。

## 显示当前的 Python 环境

```console
$ pdm info
Python Interpreter: D:/Programs/Python/Python38/python.exe (3.8.0)
Project Root:       D:/Workspace/pdm
                                                                                                                                   [10:42]
$ pdm info --env
{
  "implementation_name": "cpython",
  "implementation_version": "3.8.0",
  "os_name": "nt",
  "platform_machine": "AMD64",
  "platform_release": "10",
  "platform_system": "Windows",
  "platform_version": "10.0.18362",
  "python_full_version": "3.8.0",
  "platform_python_implementaiton": "CPython",
  "python_version": "3.8",
  "sys_platform": "win32"
}
```

## 配置项目

PDM 的 `config` 命令与 `git config` 的工作方式一样，只是不需要 `--list` 来显示配置。

显示当前的配置：

```console
pdm config
```

获得一个单一的配置：

```console
pdm config pypi.url
```

改变配置值并存储在主配置中：

```console
pdm config pypi.url "https://test.pypi.org/simple"
```

默认情况下，配置是全局性的，如果你想让配置只被这个项目看到，可以添加一个 `--local` 标志：

```console
pdm config --local pypi.url "https://test.pypi.org/simple"
```

任何本地配置将被存储在项目根目录下的 `.pdm.toml` 中。

配置文件按以下顺序进行搜索：

1. `<PROJECT_ROOT>/.pdm.toml`：项目配置
2. `~/.pdm/config.toml`：主页配置

如果使用 `-g/--global` 选项，第一项将被 `~/.pdm/global-project/.pdm.toml` 替换。

你可以在 [配置页](../configuration) 中找到所有可用的配置项目。

## 缓存轮子的安装

如果一个软件包被系统中的许多项目所需要，每个项目都必须保留自己的副本。这可能会造成磁盘空间的浪费，特别是对于数据科学和机器学习库。

PDM 支持 _caching_ 同一轮子的安装，将其安装到一个集中的包库，并在不同的项目中链接到该安装。要启用它，请运行：

```bash
pdm config feature.install_cache on
```

它可以以项目为单位，通过在命令中添加 `--local` 选项来启用。

缓存位于 `$(pdm config cache_dir)/packages` 下。人们可以通过 `pdm cache info` 查看缓存的使用情况。但是请注意，缓存的安装是自动管理的 -- 当不与任何项目连接时，它们会被删除。手动删除磁盘中的缓存可能会破坏系统中的一些项目。

```{note}
只有从 PyPI 解决的命名的需求的安装可以被缓存。
```

## 管理全局项目

有时，用户可能也想跟踪全局 Python 解释器的依赖关系。通过大多数子命令支持的 `-g/--global` 选项，用 PDM 很容易做到这一点。

如果通过该选项，`~/.pdm/global-project` 将被用作项目目录，除了 `pyproject.toml` 会自动为你创建，并且不支持构建功能外，几乎与普通项目相同。这个想法来自 Haskell 的[stack](https://docs.haskellstack.org)。

然而，与 `stack` 不同，默认情况下，如果没有找到本地项目，PDM 不会自动使用全局项目。用户应该明确传递 `-g/--global` 来激活它，因为如果软件包进入了错误的地方，这不是很令人高兴。但 PDM 也把决定权留给用户，只要把配置 `auto_global` 设为 `true` 即可。

如果你想让全局项目跟踪除 `~/.pdm/global-project` 以外的另一个项目文件，你可以通过 `-p/--project <path>` 选项提供项目路径。

```{caution}
在使用全局项目时，要小心使用 `remove` 和 `sync --clean` 命令，因为它可能会删除你的系统 Python 中安装的软件包。
```

## 在虚拟环境下工作

尽管 PDM 默认执行 {pep}`582`，但它也允许用户在 virtualenv 中安装软件包。它是由配置项 `use_venv` 控制。当它被设置为 `True` 时，PDM 将使用 virtualenv，如果：

- 一个虚拟环境已经被激活。
- `venv`、`.venv`、`env` 中的任何一个是有效的 virtualenv 文件夹。

此外，当 `use-venv` 打开，并且给出的解释器路径是类似 venv 的路径时，PDM 也会重用该 venv 目录。

对于增强的 virtualenv 支持，如 virtualenv 管理和自动创建，请选择 [pdm-venv](https://github.com/pdm-project/pdm-venv)。它可以作为一个插件安装。

## 从现有项目文件中导入项目元数据

如果你已经是其他软件包管理工具，如 Pipenv 或 Poetry，很容易迁移到 PDM。PDM 提供了 `import` 命令，这样你就不必手动初始化项目了，它现在支持：

1. Pipenv 的 `Pipfile`
2. Poetry 的部分在 `pyproject.toml`
3. Flit 的部分在 `pyproject.toml`
4. Pip 使用的 `requirements.txt` 格式

另外，当你执行 `pdm init` 或 `pdm install` 时，如果你的 PDM 项目尚未初始化，PDM 可以自动检测可能要导入的文件。如果你的 PDM 项目还没有被初始化。

## 将锁定的软件包导出为其他格式

你也可以将 `pdm.lock` 导出为其他格式，以简化 CI 流程或镜像构建过程。目前。只有 `requirements.txt` 和 `setup.py` 格式被支持。

```console
pdm export -o requirements.txt
pdm export -f setuppy -o setup.py
```

## 从 pyproject.toml 中隐藏凭证

有很多时候，我们需要使用敏感信息，例如 PyPI 服务器的登录凭证 和 VCS 仓库的用户名密码。我们不想在 `pyproject.toml` 中暴露这些信息并将其上传到 git。

PDM 提供了几种方法来实现这一点：

1. 用户可以通过环境变量给出认证信息，这些变量直接在 URL 中编码：

   ```toml
   [[tool.pdm.source]]
   url = "http://${INDEX_USER}:${INDEX_PASSWD}@test.pypi.org/simple"
   name = "test"
   verify_ssl = false

   [project]
   dependencies = [
     "mypackage @ git+http://${VCS_USER}:${VCS_PASSWD}@test.git.com/test/mypackage.git@master"
   ]
   ```

   环境变量必须以 `${ENV_NAME}` 的形式编码，其他形式不支持。此外，只有 auth 部分会被展开。

2.  如果 URL 中没有提供证书，并且从服务器收到 401 响应，当 `-v/--verbose` 作为命令行参数时，PDM 将提示用户名和密码。作为命令行参数时，PDM 将提示用户名和密码，否则 PDM 将失败，并告诉用户发生了什么。然后用户可以选择在确认问题后将证书存储在 keyring 中。

3. VCS 存储库只应用第一种方法，而索引服务器则同时应用两种方法。

## 在隔离的环境中运行脚本

通过 PDM，你可以在加载本地包的情况下运行任意的脚本或命令：

```bash
pdm run flask run -p 54321
```

PDM 也支持在 `pyproject.toml` 的可选 `[tool.pdm.scripts]` 部分的自定义脚本快捷方式。

然后你可以运行 `pdm run <shortcut_name>` 来在你的 PDM 项目中调用这个脚本。比如说：

```toml
[tool.pdm.scripts]
start_server = "flask run -p 54321"
```

然后在你的终端：

```bash
$ pdm run start_server
Flask server started at http://127.0.0.1:54321
```

任何额外的参数将被附加到命令中：

```bash
$ pdm run start_server -h 0.0.0.0
Flask server started at http://0.0.0.0:54321
```

PDM 支持 3 种类型的脚本：

### 正常命令

纯文本脚本被视为正常的命令，或者你可以明确地指定它：

```toml
[tool.pdm.scripts]
start_server = {cmd = "flask run -p 54321"}
```

在某些情况下，比如想在参数之间添加注释，将命令指定为数组而不是字符串可能更方便：

```toml
[tool.pdm.scripts]
start_server = {cmd = [
	"flask",
	"run",
	# Important comment here about always using port 54321
	"-p", "54321"
]}
```

### 外壳脚本

Shell 脚本可以用来运行更多 Shell 特有的任务，比如管道和输出重定向。这基本上是通过 `subprocess.Popen()` 与 `shell=True` 运行：

```toml
[tool.pdm.scripts]
filter_error = {shell = "cat error.log|grep CRITICAL > critical.log"}
```

### 调用 Python 函数

脚本也可以定义为以 `<module_name>:<func_name>` 的形式调用一个 python 函数：

```toml
[tool.pdm.scripts]
foobar = {call = "foo_package.bar_module:main"}
```

该函数可以提供字面参数：

```toml
[tool.pdm.scripts]
foobar = {call = "foo_package.bar_module:main('dev')"}
```

### 支持环境变量

所有在当前 shell 中设置的环境变量都可以被 `pdm run` 看到，并且在执行时将被展开。此外，你也可以在你的 `pyproject.toml` 中定义一些固定的环境变量。

```toml
[tool.pdm.scripts]
start_server.cmd = "flask run -p 54321"
start_server.env = {FOO = "bar", FLASK_ENV = "development"}
```

注意我们是如何使用 [TOML 的语法](https://github.com/toml-lang/toml) 来定义一个复合字典的。

通过 `env_file = "<file_path>"` 设置，也支持 dotenv 文件。

对于所有脚本共享的环境变量和/或 dotenv 文件，你可以在 `tool.pdm.scripts` 表的 `_` 下定义 `env` 和 `env_file`：

```toml
[tool.pdm.scripts]
_.env_file = ".env"
start_server = "flask run -p 54321"
migrate_db = "flask db upgrade"
```

此外，PDM 还通过 `PDM_PROJECT_ROOT` 环境变量注入项目的根路径。

### 在运行环境中加载 site-packages

为了确保运行环境与外部 Python 解释器正确隔离。所选解释器的站点包不会被加载到 `sys.path` 中，除非以下任何条件成立：

1. 可执行文件来自 `PATH` 但不在 `__pypackages__` 文件夹内。
2. `-s/--site-packages` 标志在 `pdm run` 之后。
3. `site_packages = true` 是在脚本表或全局设置键 `_` 中。

注意，如果运行时启用了 {pep}`582` （没有 `pdm run` 前缀），site-packages 将总是被加载。

### 显示脚本的快捷方式列表

使用 `pdm run --list/-l` 来显示可用的脚本快捷方式的列表：

```bash
$ pdm run --list
Name        Type  Script           Description
----------- ----- ---------------- ----------------------
test_cmd    cmd   flask db upgrade
test_script call  test_script:main call a python function
test_shell  shell echo $FOO        shell command
```

你可以在脚本的描述中添加一个 `help` 选项，它将显示在上述输出中的 `Description` 栏中。

## 管理缓存

PDM 提供了方便的命令组来管理缓存，有四种缓存：

1. `wheels/` 存储非轮子分布和文件的构建结果。
1. `http/` 存储 HTTP 响应内容。
1. `metadata/` 存储由解析器检索的包元数据。
1. `hashes/` 存储从软件包索引中获取的或本地计算的文件散列值。
1. `packages/` 已安装的轮子的中心化储存库。

通过输入 `pdm cache info` 查看当前的缓存使用情况。此外，你可以使用 `add`、`remove` 和 `list` 子命令来管理缓存内容。
通过每个命令的 `--help` 选项查找用法。

## 如何使 PEP 582 软件包对 Python 解释器可用

感谢 Python 启动时的 [site packages loading](https://docs.python.org/3/library/site.html)。可以通过执行 PDM 附带的 `sitecustomize.py` 来修补 `sys.path`。解释器可以在目录中搜索最近的 `__pypackage__` 文件夹并将其追加到 `sys.path` 变量中。
