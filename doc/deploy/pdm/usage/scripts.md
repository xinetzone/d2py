# PDM 脚本

像 `npm run` 一样，使用 PDM，你可以在加载本地包的情况下运行任意脚本或命令。

## 任意脚本

```bash
pdm run flask run -p 54321
```

它将在感知到的 `__pypackages__/` 文件夹中的包的环境中运行 `flask run -p 54321`。

## 用户脚本

PDM 也支持在 `pyproject.toml` 的可选 `[tool.pdm.scripts]` 部分的自定义脚本快捷方式。

然后你可以运行 `pdm run <script_name>` 来在你的 PDM 项目中调用这个脚本。比如说：

```toml
[tool.pdm.scripts]
start = "flask run -p 54321"
```

然后在你的终端：

```bash
$ pdm run start
Flask server started at http://127.0.0.1:54321
```

任何额外的参数将被附加到命令中：

```bash
$ pdm run start -h 0.0.0.0
Flask server started at http://0.0.0.0:54321
```

```{admonition} 类似于 Yarn 的脚本快捷方式
有内置快捷方式，只要脚本不与任何内置或插件贡献的命令冲突，所有脚本都可以作为根命令使用。另外，如果您有 `start` 脚本，您可以同时运行 `pdm run start` 和 `pdm start`。但是如果你有 `install` 脚本，只有 `pdm run install` 会运行它，`pdm install` 仍然会运行内置的 `install` 命令。
```

PDM 支持 4 种类型的脚本：

### `cmd`

纯文本脚本被视为正常的命令，或者你可以明确地指定它：

```toml
[tool.pdm.scripts]
start = {cmd = "flask run -p 54321"}
```

在某些情况下，比如想在参数之间添加注释，将命令指定为数组而不是字符串可能更方便：

```toml
[tool.pdm.scripts]
start = {cmd = [
	"flask",
	"run",
	# Important comment here about always using port 54321
	"-p", "54321"
]}
```

### `shell`

Shell 脚本可以用来运行更多 Shell 特有的任务，比如管道和输出重定向。这基本上是通过 `subprocess.Popen()` 与 `shell=True` 运行：

```toml
[tool.pdm.scripts]
filter_error = {shell = "cat error.log|grep CRITICAL > critical.log"}
```

### `call`

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

### `composite`

此脚本类型执行其他已定义的脚本：

```toml
[tool.pdm.scripts]
lint = "flake8"
test = "pytest"
all = {composite = ["lint", "test"]}
```

运行 `pdm run all` 将先运行 `lint` ，如果 `lint`  成功，则再运行 `test`。

也可以为被调用的脚本提供参数：

```toml
[tool.pdm.scripts]
lint = "flake8"
test = "pytest"
all = {composite = ["lint mypackage/", "test -v tests/"]}
```

```{note}
参数传递给每个被调用的任务。
```

## 脚本选项

### `env`

所有在当前 shell 中设置的环境变量都可以被 `pdm run` 看到，并且在执行时将被展开。此外，你也可以在你的 `pyproject.toml` 中定义一些固定的环境变量。

```toml
[tool.pdm.scripts]
start.cmd = "flask run -p 54321"
start.env = {FOO = "bar", FLASK_ENV = "development"}
```

注意我们是如何使用 [TOML 的语法](https://github.com/toml-lang/toml) 来定义一个复合字典的。

```{note}
在复合任务级别上指定的环境变量将覆盖被调用任务定义的环境变量。
```

### `env_file`

您也可以将所有环境变量存储在 dotenv 文件中，并让 PDM 读取它：

```toml
[tool.pdm.scripts]
start.cmd = "flask run -p 54321"
start.env_file = ".env"
```

dotenv 文件中的变量将不会覆盖任何现有的环境变量。如果你想让 dotenv 文件覆盖现有的环境变量，请使用以下方法：

```toml
[tool.pdm.scripts]
start.cmd = "flask run -p 54321"
start.env_file.override = ".env"
```

```{note}
复合任务级别上指定的 dotenv 文件将覆盖被调用任务定义的 dotenv 文件。
```


### `site_packages`

为了确保运行环境与外部 Python 解释器正确隔离。所选解释器的站点包不会被加载到 `sys.path` 中，除非以下任何条件成立：

1. 可执行文件来自 `PATH` 但不在 `__pypackages__` 文件夹内。
2. `-s/--site-packages` 标志在 `pdm run` 之后。
3. `site_packages = true` 是在脚本表或全局设置键 `_` 中。

注意，如果运行时启用了 {pep}`582` （没有 `pdm run` 前缀），site-packages 将总是被加载。

### 共享选项

如果你想让 `pdm run` 运行的所有任务共享这些选项，你可以把它们写在 `[tool.pdm.scripts]` 表中的特殊键 `_` 下：

```toml
[tool.pdm.scripts]
_.env_file = ".env"
start = "flask run -p 54321"
migrate_db = "flask db upgrade"
```

此外，在任务内部，`PDM_PROJECT_ROOT` 环境变量将被设置为项目根。

### 参数占位符

默认情况下，所有用户提供的额外参数都被简单地附加到命令（或用于 `composite` 任务的所有命令）。

如果你想对用户提供的额外参数有更多的控制，你可以使用 `{args}` 占位符。它适用于所有脚本类型，并将正确地为每种脚本插入：

```toml
[tool.pdm.scripts]
cmd = "echo '--before {args} --after'"
shell = {shell = "echo '--before {args} --after'"}
composite = {composite = ["cmd --something", "shell {args}"]}
```

将产生以下插值（那些不是真正的脚本，只是在这里说明插值）：

```shell
$ pdm run cmd --user --provided
--before --user --provided --after
$ pdm run cmd
--before --after
$ pdm run shell --user --provided
--before --user --provided --after
$ pdm run shell
--before --after
$ pdm run composite --user --provided
cmd --something
shell --before --user --provided --after
$ pdm run composite
cmd --something
shell --before --after
```

如果没有提供用户参数，您可以选择提供默认值：

```toml
[tool.pdm.scripts]
test = "echo '--before {args:--default --value} --after'"
```

将产生以下内容：

```shell
$ pdm run test --user --provided
--before --user --provided --after
$ pdm run test
--before --default --value --after
```

```{note}
一旦检测到占位符，参数就不再追加。这对于 `composite` 脚本很重要，因为如果在子任务上检测到占位符，那么子任务中没有任何子任务会附加参数，您需要显式地将占位符传递给每个需要它的嵌套命令。
```

```{note}
`call` 脚本不支持 `{args}` 占位符，因为它们可以访问 `sys.argv` 直接处理这种复杂的情况和更多。
```

### 显示脚本的快捷方式列表

使用 `pdm run --list/-l` 来显示可用的脚本快捷方式的列表：

```bash
$ pdm run --list
╭─────────────┬───────┬───────────────────────────╮
│ Name        │ Type  │ Description               │
├─────────────┼───────┼───────────────────────────┤
│ test_cmd    │ cmd   │ flask db upgrade          │
│ test_script │ call  │ call a python function    │
│ test_shell  │ shell │ shell command             │
╰─────────────┴───────┴───────────────────────────╯
```

你可以在脚本的描述中添加一个 `help` 选项，它将显示在上述输出中的 `Description` 栏中。

## Pre & Post 脚本

像 `npm` 一样，PDM 也支持通过前置和后发脚本组成任务，前置脚本将在给定任务之前运行，后发脚本将在给定任务之后运行。

```toml
[tool.pdm.scripts]
pre_compress = "{{ Run BEFORE the `compress` script }}"
compress = "tar czvf compressed.tar.gz data/"
post_compress = "{{ Run AFTER the `compress` script }}"
```

在本例中，`pdm run compress` 将依次运行所有这 3 个脚本。

```{admonition} 管道快速失效
在预自后脚本的管道中，失败将取消后续的执行。
```

## 脚本钩子

在某些情况下，PDM 会寻找一些特殊的钩子脚本来执行：

- `post_init`: Run after `pdm init`
- `pre_install`: Run before installing packages
- `post_install`: Run after packages are installed
- `pre_lock`: Run before dependency resolution
- `post_lock`: Run after dependency resolution
- `pre_build`: Run before building distributions
- `post_build`: Run after distributions are built
- `pre_publish`: Run before publishinbg distributions
- `post_publish`: Run after distributions are published
- `pre_script`: Run before any script
- `post_script`: Run after any script
- `pre_run`: Run once before run script invocation
- `post_script`: Run once after run script invocation

```{note}
Pre & post 脚本不能接收任何参数。
```

```{admonition} 避免名称冲突
如果在 `[tool.pdm.scripts]` 下存在 `install` 脚本，`pre_install` 脚本可以由 `pdm install` 和 `pdm run install` 触发。因此建议不要使用保留的名称。
```

```{note}
复合任务还可以有前置脚本和后置脚本。

被调用的任务将运行它们自己的前置和后置脚本。
```

## 跳过脚本

因为，有时需要运行脚本，但不包含钩子或 pre 和 post 脚本，这里有 `--skip=:all`，它将禁用所有钩子，pre 和 post。还有 `--skip=:pre` 和 `--skip=:post` 分别允许跳过所有  `pre_*` 钩子和所有 `post_*` 钩子。

也可能需要前置脚本而不需要后脚本，或者需要组合任务中的所有任务。对于这些用例，有更细粒度的 `--skip` 参数，接受要排除的任务或钩子名称列表。

```bash
pdm run --skip pre_task1,task2 my-composite
```

这个命令将运行 `my-composite` 任务，并跳过 `pre_task1` 钩子以及 `task2` 及其钩子。

你也可以在 `PDM_SKIP_HOOKS` 环境变量中提供你的跳过列表，但一旦提供了 `--skip` 参数，它就会被覆盖。

在 [专用钩子页面](hooks.md) 上有更多关于钩子和前/后脚本行为的细节。
