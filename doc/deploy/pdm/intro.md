# PDM 简介

[PDM](https://github.com/pdm-project/pdm) 为现代 Python 软件包管理工具。它以类似于 `npm` 的方式安装和管理软件包，完全不需要创建虚拟环境！它是一个非常好的解决方案。

```{admonition} 特性
- {pep}`582` 本地软件包安装器和运行器，完全不需要虚拟环境（用 `__pypackages__` 目录代替虚拟环境进行软件包安装）。
- 简单且相对快速的依赖关系解析器，主要用于大型二进制发行版。
- 兼容 {pep}`517` 的构建后端，用于构建发布包（源码格式与 wheel 格式）。
- {pep}`621` 项目元数据。
- 灵活而强大的插件系统。
- 像 [pnpm] 一样的中心化安装缓存，节省磁盘空间。

[pnpm]: https://pnpm.io/motivation#saving-disk-space-and-boosting-installation-speed
```

## 安装 PDM

PDM 需要安装 Python 3.7+。它可以在多个平台上工作，包括 Windows、Linux 和 MacOS。

```{note}
对于你的项目使用的 Python 版本没有限制，但安装 PDM 本身推荐使用 Python 3.7 以上。
```

### 建议的安装方法

PDM 要求 python 3.7 或更高版本。

和 Pip 一样，PDM 提供了安装脚本，将 PDM 安装到隔离的环境中。

`````{tab-set}
````{tab-item} Linux/Mac
```bash
curl -sSL https://raw.githubusercontent.com/pdm-project/pdm/main/install-pdm.py | python3 -
```
````

````{tab-item} Windows
```bash
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/pdm-project/pdm/main/install-pdm.py -UseBasicParsing).Content | python -
```
````
`````

安装程序将把 PDM 安装到用户站点，位置取决于系统：

- Unix：`$HOME/.local/bin`
- Windows：`%APPDATA%\Python\Scripts`

其他安装方式：

`````{tab-set}
````{tab-item} Homebrew
```bash
brew install pdm
```
````

````{tab-item} Scoop
```bash
scoop bucket add frostming https://github.com/frostming/scoop-frostming.git
scoop install pdm
```
````

````{tab-item} pipx
```bash
pipx install pdm
```
````
````{tab-item} pip
```bash
pip install --user pdm
```
````
`````

**支持 Unicode 和 ANSI**：PDM 在 ANSI 字符和 unicode emojis 的帮助下提供了一个花哨的终端 UI。它可以自动打开/关闭，取决于你的终端是否支持它。然而，如果你看到任何乱码的字符，设置 env var `DISABLE_UNICODE_OUTPUT=1` 来关闭它。

### 更新 PDM 版本

```bash
pdm self update
```

## PDM Shell 自动补全

PDM 支持为 Bash、Zsh、Fish 或 Powershell 生成完成脚本。下面是每个 shell 的一些常用位置。

`````{tab-set}
````{tab-item} Bash
```bash
pdm completion bash > /etc/bash_completion.d/pdm.bash-completion
```
````
````{tab-item} PowerShell
```bash
# Create a directory to store completion scripts
mkdir $PROFILE\..\Completions
echo @'
Get-ChildItem "$PROFILE\..\Completions\" | ForEach-Object {
    . $_.FullName
}
'@ | Out-File -Append -Encoding utf8 $PROFILE
# Generate script
Set-ExecutionPolicy Unrestricted -Scope CurrentUser
pdm completion powershell | Out-File -Encoding utf8 $PROFILE\..\Completions\pdm_completion.ps1
```
````
````{tab-item} Zsh
```bash
# Make sure ~/.zfunc is added to fpath, before compinit.
pdm completion zsh > ~/.zfunc/_pdm
```
````
````{tab-item} Fish
```bash
pdm completion fish > ~/.config/fish/completions/pdm.fish
```
````
`````

## 快速上手

```{rubric} 初始化新的 PDM 项目
```

```bash
pdm init
```

按照指引回答提示的问题，PDM 项目和对应的 `pyproject.toml` 文件就创建好了。

```{rubric} 添加依赖
```

```bash
pdm add requests flask
```

你可以在同一条命令中添加多个依赖。稍等片刻完成之后，你可以查看 `pdm.lock` 文件看看有哪些依赖以及对应版本。

## PDM 生态

[Awesome PDM](https://github.com/pdm-project/awesome-pdm) 是精心策划的 PDM 插件和资源的列表。
