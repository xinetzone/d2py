# 打包

## 打包准备

1. 确保 Python 正确安装：

`````{tab-set} 
````{tab-item} CMD
```bash
python --version
```
````

````{tab-item} IPython/Jupyter
```bash
import sys
!{sys.executable} --version
```
````
`````

2. 确保 `pip` 可用：

```bash
python -m pip --version
```

若 `pip` 没有安装，则可以（或者其他方法）：

```bash
python -m ensurepip --default-pip
```

3. 确保 pip、setuptools 和 wheel 是最新的：

```bash
python -m pip install --upgrade pip setuptools wheel
```

4. 可选地，创建一个虚拟环境

```bash
python -m venv tutorial_env
```

`````{tab-set} 
````{tab-item} Unix/macOS
```bash
source tutorial_env/bin/activate
```
````
````{tab-item} Windows
```bash
tutorial_env\Scripts\activate
```
````
`````

## 创建虚拟环境

Python “虚拟环境” 允许 Python 包 为特定的应用程序安装在一个孤立的位置，而不是全局安装。

* [venv](https://docs.python.org/3/library/venv.html "(在 Python v3.10)") 在 Python 3.3 及以后的版本中默认可用，并在 Python 3.4 及以后的版本中把 [pip](https://daobook.github.io/packaging.python.org/key_projects.html#pip) 和 [setuptools](https://daobook.github.io/packaging.python.org/key_projects.html#setuptools) 安装到创建的虚拟环境中。

## 打包工具

### [Pipenv](https://pipenv.pypa.io) 项目

Pipenv 是一个依赖管理器，它结合了 `pip` 和 `venv`，正如其名称所暗示的。它可以从一种自定义格式文件 `Pipfile.lock` 或 `Pipfile` 中安装软件包。然而，Pipenv 并不处理任何与构建、打包和发布相关的工作。所以它只适用于开发不可安装的应用程序（例如 Django 网站）。如果你是库的开发者，无论如何你都需要 `setuptools`。

### [Poetry](https://python-poetry.org) 项目

Poetry 以类似于 Pipenv 的方式管理环境和依赖，它也可以从你的代码构建 `.whl` 文件，并且可以将轮子和源码发行版上传到 PyPI。它有漂亮的用户界面，用户可以通过贡献插件来定制它。Poetry 使用 `pyproject.toml` 标准。但它并不遵循指定元数据应如何在 `pyproject.toml` 文件中表示的标准（{pep}`621`）。而是使用一个自定义的 `[tool.poetry]` 表。这部分是因为 Poetry 诞生在 {pep}`621` 出现之前。

[安装](https://python-poetry.org/docs/#installation)：

```bash
pipx install poetry
```

更新 Poetry：

```bash
poetry self update
```

为 Bash、Fish 或 Zsh 启用自动补全功能：

```bash
# Bash
poetry completions bash > /etc/bash_completion.d/poetry.bash-completion

# Bash (Homebrew)
poetry completions bash > $(brew --prefix)/etc/bash_completion.d/poetry.bash-completion

# Fish
poetry completions fish > ~/.config/fish/completions/poetry.fish

# Fish (Homebrew)
poetry completions fish > (brew --prefix)/share/fish/vendor_completions.d/poetry.fish

# Zsh
poetry completions zsh > ~/.zfunc/_poetry

# Oh-My-Zsh
mkdir $ZSH_CUSTOM/plugins/poetry
poetry completions zsh > $ZSH_CUSTOM/plugins/poetry/_poetry

# prezto
poetry completions zsh > ~/.zprezto/modules/completion/external/src/_poetry
```

### [Hatch](https://hatch.pypa.io) 项目

Hatch([Hatch 中文](https://daobook.github.io/hatch/dev) ) 也可以管理环境（它允许每个项目有多个环境，但不允许把它们放在项目目录中），并且可以管理包（但不支持 lockfile）。Hatch 也可以用来打包项目（用符合 {pep}`621` 标准的 `pyproject.toml` 文件）并上传到 PyPI。

对项目管理工作流程中更多的步骤进行了观点上的覆盖，如递增版本、标记发布，以及从项目模板创建新的骨架项目。

Hatch 是现代的、可扩展的 Python 项目管理器。支持：

- 标准化的 [构建系统](https://daobook.github.io/hatch/dev/dev/build/#packaging-ecosystem)，默认为可重复构建
- 强大的 [环境管理](https://daobook.github.io/hatch/dev/dev/environment/)，支持自定义脚本
- 轻松 [发布](https://daobook.github.io/hatch/dev/dev/publish/) 到 PyPI 或其他资源
- [版本管理](https://daobook.github.io/hatch/dev/dev/version/)
- 可配置的 [项目生成](https://daobook.github.io/hatch/dev/dev/config/project-templates/)，具有合理的默认值
- 反应灵敏的 CLI，比同等工具快 2-3 倍

[安装](https://daobook.github.io/hatch/dev/dev/install/)：

```bash
pipx install hatch
```

### [PDM 项目](pdm/index)

PDM 也可以像 Pipenv 那样在项目或集中的位置管理 venvs。它从一个标准化的 `pyproject.toml` 文件中读取项目元数据，并支持 lockfile。用户可以在插件中添加更多的功能，并将其作为一个发行版上传，以供分享。此外，PDM有一个实验性的 [PEP 582] 支持（[docs](https://pdm.fming.dev/latest/usage/pep582/)），这意味着你可以在不创建虚拟环境的情况下安装包。此外，与 Poetry 和 Hatch 不同，PDM 并没有和特定的构建后端绑定，你可以选择任何你喜欢的构建后端。

### 其他打包项目

参考：[packaging](https://daobook.github.io/packaging.python.org/key_projects.html#flit)

- [Flit](https://github.com/daobook/flit) 是一种将 Python 包和模块放在 PyPI 上的简单方法。它试图让你在打包时少花心思，并帮助你避免常见的错误。
- [micropipenv](https://github.com/thoth-station/micropipenv) for a lightweight wrapper around pip that supports `requirements.txt`, Pipenv and Poetry lock files, or converting them to pip-tools compatible output. Designed for containerized Python applications, but not limited to them.
- [pex](https://daobook.github.io/pex/) 是 “Python Executable” 的缩写。它提供了通用 Python 环境虚拟化解决方案。
