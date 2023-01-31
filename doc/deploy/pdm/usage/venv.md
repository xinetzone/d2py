# PDM 中使用虚拟环境

当您运行 `pdm init` 命令时，pdm 将要求在项目中[使用 Python 解释器](pdm:choose-a-python-interpreter)，这是安装依赖项和运行任务的基本解释器。

与 {pep}`582` 相比，虚拟环境被认为更成熟，并且在 Python 生态系统和 IDE 中有更好的支持。因此，如果未配置 virtualenv 模式，则默认为 virtualenv 模式。

**如果项目解释器（存储在 `.pdm.toml` 中的解释器，可使用 `pdm info` 查看）被使用，则将使用虚拟环境。**

## 自动创建虚拟环境

默认情况下，PDM 倾向于像其他包管理器一样使用 virtualenv 布局。当你第一次在新的 pdm 管理的项目上运行 `pdm install` 时，它的 Python 解释器还没有确定，pdm 将在 `<project_root>/.venv` 目录下创建 virtualenv。Venv，并在其中安装依赖项。在 `pdm init` 的交互会话中，pdm 还会要求为您创建 virtualenv。

您可以选择 PDM 用于创建 virtualenv 的后端。目前它支持三个后端：

- [`virtualenv`](https://virtualenv.pypa.io/)(default)
- `venv`
- `conda`

您可以通过 `pdm config venv.backend [virtualenv|venv|conda]` 更改它。

## 自己创建 virtualenv

你可以用你想要的任何 Python 版本创建多个虚拟环境：

```bash
# Create a virtualenv based on 3.8 interpreter
$ pdm venv create 3.8
# Assign a different name other than the version string
$ pdm venv create --name for-test 3.8
# Use venv as the backend to create, support 3 backends: virtualenv(default), venv, conda
$ pdm venv create --with venv 3.9
```

## virtualenv 的位置

PDM 将第一次尝试在项目中创建 virtualenv，除非 `.venv` 已经存在。其他 virtualenv 将转到 `venv.location` 配置。它们被命名为 `<project_name>-<path_hash>-<name_or_python_version>` 避免名称冲突。使用 `--name` 选项创建的 virtualenv 将始终到此位置。您可以通过 `pdm config venv.in_project false` 禁用在项目中创建 virtualenv。

## 自动检测虚拟环境

当项目配置中没有存储解释器或设置了 `PDM_IGNORE_SAVED_PYTHON` env var 时，PDM 将尝试检测可能使用的 virtualenv：

- 项目根目录的文件夹 `venv`, `env`, `.venv`
- 当前激活的 virtualenv

## 列出用这个项目创建的所有 virtualenv

```bash
$ pdm venv list
Virtualenvs created with this project:

-  3.8.6: C:\Users\Frost Ming\AppData\Local\pdm\pdm\venvs\test-project-8Sgn_62n-3.8.6
-  for-test: C:\Users\Frost Ming\AppData\Local\pdm\pdm\venvs\test-project-8Sgn_62n-for-test
-  3.9.1: C:\Users\Frost Ming\AppData\Local\pdm\pdm\venvs\test-project-8Sgn_62n-3.9.1
```

## 移除 virtualenv

```bash
$ pdm venv remove for-test
Virtualenvs created with this project:
Will remove: C:\Users\Frost Ming\AppData\Local\pdm\pdm\venvs\test-project-8Sgn_62n-for-test, continue? [y/N]:y
Removed C:\Users\Frost Ming\AppData\Local\pdm\pdm\venvs\test-project-8Sgn_62n-for-test
```

## 激活 virtualenv

`pdm-venv` 不像 `pipenv` 和 `poetry` 那样生成子 shell，而是为您创建 shell，并将激活命令打印到控制台。这样就不会离开当前的外壳。然后你可以把输出给 `eval` 来激活 virtualenv：

`````{tab-set}
````{tab-item} bash/csh/zsh
```bash
$ eval $(pdm venv activate for-test)
(test-project-for-test) $  # Virtualenv entered
```
````
````{tab-item} Fish
```fish
$ eval (pdm venv activate for-test)
```
````
````{tab-item} Powershell
```ps1
PS1> Invoke-Expression (pdm venv activate for-test)
```

您可以自己制作 shell 快捷功能，避免长命令的输入。下面是 Bash 的例子：

```ps1
pdm_venv_activate() {
    eval $('pdm' 'venv' 'activate' "$1")
}
```

然后，您可以通过  `pdm_venv_activate $venv_name` 激活它，并直接通过 deactivate 禁用它。

此外，如果项目解释器是 venv Python，则可以省略 activate 后面的 name 参数。
````
`````

```{note}
`venv activate` **不会** 切换项目使用的 Python 解释器。它只通过将 virtualenv 路径注入环境变量来更改 shell。对于上述目的，使用 `pdm use` 命令。
```

有关 CLI 的更多用法，请参阅 `pdm venv` 文档。

## 定制 Prompt

默认情况下，当你激活 virtualenv 时，提示将显示：`{project_name}-{python_version}`。

例如，如果你的项目名为 `test-project`：

```bash
$ eval $(pdm venv activate for-test)
(test-project-3.10) $  # {project_name} == test-project and {python_version} == 3.10
```

在使用 [`venv.prompt`](configuration) 提示配置或 `PDM_VENV_PROMPT` 环境变量(在 `pdm init` 或 `pdm venv create` 之前) 创建自定义格式。可选变量包括：

 - `project_name`: name of your project
 - `python_version`: version of Python (used by the virtualenv)

```bash
$ PDM_VENV_PROMPT='{project_name}-py{python_version}' pdm venv create --name test-prompt
$ eval $(pdm venv activate test-prompt)
(test-project-py3.10) $
```

## 禁用 virtualenv 模式

您可以使用 `pdm config python.use_venv false` 禁用 virtualenv 自动创建和自动检测功能。**如果 venv 被禁用，即使所选解释器来自 virtualenv, PEP 582 模式也将始终使用。**
