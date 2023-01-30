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

For the first time, PDM will try to create a virtualenv **in project**, unless `.venv` already exists.
Other virtualenvs go to the location specified by the `venv.location` configuration. They are named as `<project_name>-<path_hash>-<name_or_python_version>` to avoid name collision. A virtualenv created with `--name` option will always go to this location. You can disable the in-project virtualenv creation by `pdm config venv.in_project false`.

## Virtualenv auto-detection

When no interpreter is stored in the project config or `PDM_IGNORE_SAVED_PYTHON` env var is set, PDM will try to detect possible virtualenvs to use:

- `venv`, `env`, `.venv` directories in the project root
- The currently activated virtualenv

## List all virtualenvs created with this project

```bash
$ pdm venv list
Virtualenvs created with this project:

-  3.8.6: C:\Users\Frost Ming\AppData\Local\pdm\pdm\venvs\test-project-8Sgn_62n-3.8.6
-  for-test: C:\Users\Frost Ming\AppData\Local\pdm\pdm\venvs\test-project-8Sgn_62n-for-test
-  3.9.1: C:\Users\Frost Ming\AppData\Local\pdm\pdm\venvs\test-project-8Sgn_62n-3.9.1
```

## Remove a virtualenv

```bash
$ pdm venv remove for-test
Virtualenvs created with this project:
Will remove: C:\Users\Frost Ming\AppData\Local\pdm\pdm\venvs\test-project-8Sgn_62n-for-test, continue? [y/N]:y
Removed C:\Users\Frost Ming\AppData\Local\pdm\pdm\venvs\test-project-8Sgn_62n-for-test
```

## Activate a virtualenv

Instead of spawning a subshell like what `pipenv` and `poetry` do, `pdm-venv` doesn't create the shell for you but print the activate command to the console. In this way you won't leave the current shell. You can then feed the output to `eval` to activate the virtualenv:

`````{tab-set}
````{tab-item} bash/csh/zsh
```bash
$ eval $(pdm venv activate for-test)
(test-project-for-test) $  # Virtualenv entered
Fish

$ eval (pdm venv activate for-test)
```
````
````{tab-item} Powershell
```ps1
PS1> Invoke-Expression (pdm venv activate for-test)
```

You can make your own shell shortcut function to avoid the input of long command. Here is an example of Bash:

```ps1
pdm_venv_activate() {
    eval $('pdm' 'venv' 'activate' "$1")
}
```

Then you can activate it by `pdm_venv_activate $venv_name` and deactivate by deactivate directly.

Additionally, if the project interpreter is a venv Python, you can omit the name argument following activate.
````
`````

```{note}
`venv activate` **does not** switch the Python interpreter used by the project. It only changes the shell by injecting the virtualenv paths to environment variables. For the forementioned purpose, use the `pdm use` command.
```
For more CLI usage, see the [`pdm venv`](cli_reference.md#exec-0--venv) documentation.

## Prompt customization

By default when you activate a virtualenv, the prompt will show: `{project_name}-{python_version}`.

For example if your project is named `test-project`:

```bash
$ eval $(pdm venv activate for-test)
(test-project-3.10) $  # {project_name} == test-project and {python_version} == 3.10
```

The format can be customized before virtualenv creation with the [`venv.prompt`](configuration.md) configuration or `PDM_VENV_PROMPT` environment variable (before a `pdm init` or `pdm venv create`).
Available variables are:

 - `project_name`: name of your project
 - `python_version`: version of Python (used by the virtualenv)

```bash
$ PDM_VENV_PROMPT='{project_name}-py{python_version}' pdm venv create --name test-prompt
$ eval $(pdm venv activate test-prompt)
(test-project-py3.10) $
```

## Disable virtualenv mode

You can disable the auto-creation and auto-detection for virtualenv by `pdm config python.use_venv false`.
**If venv is disabled, PEP 582 mode will always be used even if the selected interpreter is from a virtualenv.**
