# 打包

## 准备

1. 确保 Python 正确安装：

````{tab} CMD
```bash
python --version
```
````

````{tab} IPython/Jupyter
```bash
import sys
!{sys.executable} --version
```
````

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

````{tab} Unix/macOS
```bash
source tutorial_env/bin/activate
```
````

````{tab} Windows
```bash
tutorial_env\Scripts\activate
```
````

## 创建虚拟环境

Python “虚拟环境” 允许 Python 包 为特定的应用程序安装在一个孤立的位置，而不是全局安装。

* [venv](https://docs.python.org/3/library/venv.html "(在 Python v3.10)") 在 Python 3.3 及以后的版本中默认可用，并在 Python 3.4 及以后的版本中把 [pip](https://daobook.github.io/packaging.python.org/key_projects.html#pip) 和 [setuptools](https://daobook.github.io/packaging.python.org/key_projects.html#setuptools) 安装到创建的虚拟环境中。

## 打包工具

参考：[packaging](https://daobook.github.io/packaging.python.org/key_projects.html#flit)

- [Flit](https://github.com/daobook/flit) 是一种将 Python 包和模块放在 PyPI 上的简单方法。它试图让你在打包时少花心思，并帮助你避免常见的错误。
- [micropipenv](https://github.com/thoth-station/micropipenv) for a lightweight wrapper around pip that supports `requirements.txt`, Pipenv and Poetry lock files, or converting them to pip-tools compatible output. Designed for containerized Python applications, but not limited to them.
- [pex](https://daobook.github.io/pex/) 是 “Python Executable” 的缩写。它提供了通用 Python 环境虚拟化解决方案。

### Poetry

[Poetry](https://github.com/python-poetry/poetry) 是一个与 Pipenv 范围相当的工具，它更直接地关注于被管理的项目被结构化为一个可分发的 Python 包，并有一个有效的 `pyproject.toml` 文件。相比之下，Pipenv 明确地避免了这样的假设：正在工作的应用程序将支持作为一个 `pip` 可安装的 Python 包发布。

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

### Hatch

[Hatch](https://github.com/ofek/hatch) 对项目管理工作流程中更多的步骤进行了观点上的覆盖，如递增版本、标记发布，以及从项目模板创建新的骨架项目。

Hatch 是一个现代的、可扩展的 Python 项目管理器。支持：

- 标准化的 [构建系统](https://ofek.dev/hatch/dev/build/#packaging-ecosystem)，默认为可重复构建
- 强大的 [环境管理](https://ofek.dev/hatch/dev/environment/)，支持自定义脚本
- 轻松 [发布](https://ofek.dev/hatch/dev/publish/) 到 PyPI 或其他资源
- [版本管理](https://ofek.dev/hatch/dev/version/)
- 可配置的 [项目生成](https://ofek.dev/hatch/dev/config/project-templates/)，具有合理的默认值
- 反应灵敏的 CLI，比同等工具快 2-3 倍

[安装](https://ofek.dev/hatch/dev/install/)：

```bash
pipx install hatch
```
