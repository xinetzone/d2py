# 简介

[PDM](https://github.com/pdm-project/pdm) 为现代 Python 软件包管理工具，支持 {pep}`582` （用 `__pypackages__` 目录代替虚拟环境进行软件包安装），并依赖于 {pep}`517` 和 {pep}`621` 等标准。它以类似于 `npm` 的方式安装和管理软件包，完全不需要创建一个虚拟环境！它是一个非常好的解决方案。

特性：

- {pep}`582` 本地软件包安装器和运行器，完全不涉及 virtualenv。
- 简单且相对快速的依赖关系解析器，主要用于大型二进制发行版。
- {pep}`517` 的构建后端。
- {pep}`621` 项目元数据。
- 灵活而强大的插件系统。
- 像 `pnpm` 一样选择集中式安装缓存。

## 安装

PDM需要安装 Python 3.7+。它可以在多个平台上工作，包括 Windows、Linux 和 MacOS。

```{note}
对于你的项目使用的 Python 版本没有限制，但安装 PDM 本身需要 Python 3.7 以上。
```

### 建议的安装方法

PDM 要求 python 3.7 或更高版本。

和 Pip 一样，PDM 提供了一个安装脚本，将 PDM 安装到一个隔离的环境中。

````{tab} Linux/Mac
```bash
curl -sSL https://raw.githubusercontent.com/pdm-project/pdm/main/install-pdm.py | python3 -
```
````

````{tab} Windows
```bash
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/pdm-project/pdm/main/install-pdm.py -UseBasicParsing).Content | python -
```
````

安装程序将把PDM安装到用户站点，位置取决于系统：

- Unix：`$HOME/.local/bin`
- Windows：`%APPDATA%\Python\Scripts`

其他安装方式：

````{tab} Homebrew
```bash
brew install pdm
```
````

````{tab} Scoop
```bash
scoop bucket add frostming https://github.com/frostming/scoop-frostming.git
scoop install pdm
```
````

````{tab} pipx
```bash
pipx install pdm
```
````
````{tab} pip
```bash
pip install --user pdm
```
````

PDM 支持为 Bash、Zsh、Fish 或 Powershell 生成完成脚本。下面是每个 shell 的一些常用位置。

````{tab} Bash
```bash
pdm completion bash > /etc/bash_completion.d/pdm.bash-completion
```
````

````{tab} PowerShell
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

**支持 Unicode 和 ANSI**：PDM 在 ANSI 字符和 unicode emojis 的帮助下提供了一个花哨的终端 UI。它可以自动打开/关闭，取决于你的终端是否支持它。然而，如果你看到任何乱码的字符，设置 env var `DISABLE_UNICODE_OUTPUT=1` 来关闭它。

## 使用 IDE

现在在大多数 IDE 中都没有对 PEP 582 的内置支持或插件，你必须手动配置你的工具。

PDM 会在 `.pdm.toml` 中写入并存储整个项目的配置，建议你在 `.gitignore` 中添加以下几行：

```
.pdm.toml
__pypackages__/
```

## VSCode

在 `.vscode/settings.json` 的顶层 dict 中添加以下两个条目：

```json
{
  "python.autoComplete.extraPaths": ["__pypackages__/<major.minor>/lib"],
  "python.analysis.extraPaths": ["__pypackages__/<major.minor>/lib"]
}
```

在全局范围内启用 PEP582，并确保 VSCode 使用与你启用 PEP582 相同的用户和 Shell 运行。

此外，还有一个 [VSCode 任务提供者](https://marketplace.visualstudio.com/items?itemName=knowsuchagency.pdm-task-provider) 扩展可供下载。

这使得 VSCode 可以自动检测 [pdm 脚本](https://pdm.fming.dev/project/#run-scripts-in-isolated-environment)，从而使它们可以作为 [VSCode 任务](https://code.visualstudio.com/docs/editor/tasks)原生运行。

## 生态

[Awesome PDM](https://github.com/pdm-project/awesome-pdm) 是一个精心策划的 PDM 插件和资源的列表。
