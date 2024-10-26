# 管理依赖

参考：[依赖](https://pdm.fming.dev/usage/dependency/)

PDM 提供了一堆手写的命令来帮助管理你的项目和依赖关系。下面的例子是在 Ubuntu 18.04 上运行的，如果你使用的是 Windows，必须做一些改变。

## 初始化项目

```bash
mkdir pdm-test && cd pdm-test
pdm init
```

回答 PDM 提出的几个问题，在项目根部将为你创建一个 `pyproject.toml`。

```toml
[project]
name = "pdm-test"
version = "0.1.0"
description = ""
authors = [
    {name = "xinetzone", email = "xinzone@outlook.com"},
]
dependencies = []
requires-python = ">=3.10"
license = {text = "MIT"}

[project.urls]
homepage = ""

[tool]
[tool.pdm]

[build-system]
requires = ["pdm-pep517"]
build-backend = "pdm.pep517.api"
```

如果 `pyproject.toml` 已经存在，它将被更新为元数据。元数据的格式遵循 {pep}`621` 的规范。

关于 `pyproject.toml` 中每个字段的详细含义，请参考[项目文件](https://pdm.fming.dev/pyproject/pep621/)。

## 添加依赖

```bash
pdm add requests
```

`pdm add` 后面可以有一个或几个依赖关系，依赖关系规范在 {pep}`508` 中描述。

PDM 也允许通过提供 `-G/--group <name>` 选项来实现额外的依赖组，这些依赖将分别进入项目文件中的 `[project.optional-dependencies.<name>]` 表。

之后，依赖关系和子依赖关系将被正确解决，并为你安装，你可以查看 `pdm.lock` 以查看所有依赖关系的解决结果。

### 添加本地依赖

本地软件包可以用它们的路径添加：

```bash
pdm add ./sub-package
```

本地软件包可以在可编辑模式下安装（就像 `pip install -e <local project path>` 那样），使用 `pdm add -e/--editable <local project path>`。

### 添加仅用于开发的依赖性

PDM 也支持定义对开发有用的依赖关系组，例如，一些用于测试，另一些用于 linting。我们通常不希望这些依赖关系出现在发行版的元数据中，所以使用 `optional-dependencies` 可能不是一个好主意。我们可以把它们定义为开发依赖：

```bash
pdm add -dG test pytest
```

这将导致 `pyproject.toml` 出现：

```toml
[tool.pdm.dev-dependencies]
test = ["pytest"]
```

为了向后兼容，如果只指定了 `-d` 或 `--dev`，依赖将默认转到 `[tool.pdm.dev-dependencies]` 下的 `dev` 组。

```{note}
相同的组名不能同时出现在 `[tool.pdm.dev-dependencies]` 和 `[project.optional-dependencies]` 中。
```

### 保存版本说明

如果软件包没有像 `pdm add requests` 那样给出版本说明。PDM 提供了三种不同的行为，即为依赖关系保存什么样的版本说明，这由 `--save-<strategy>` 给出（假设 `2.21.0` 是可以找到的依赖关系的最新版本）：

- `minimum`：保存最小的版本说明，即 `>=2.21.0` （默认）。
- `compatible`：保存兼容的版本说明，如 `>=2.21.0,<3.0.0`。
- `exact`：保存精确的版本说明，如 `==2.21.0`。
- `wildcard`：不限制版本，让指定符成为通配符 `*`。

### 添加预发布

人们可以给 `pdm add` 提供 `--pre/--prerelease` 选项，以便允许为给定的软件包钉上预发布。

(pdm:update-existing-dependencies)=
## 更新已有依赖

要更新锁文件中的所有依赖关系：

```bash
pdm update
```

要更新指定的软件包：

```bash
pdm update requests
```

要更新多组依赖关系：

```bash
pdm update -G security -G http
```

更新指定组中的某个包：

```bash
pdm update -G security cryptography
```

如果没有给出组，PDM 将在默认的依赖关系集中搜索需求，如果没有找到，则会引发错误。

要更新开发依赖中的软件包：

```bash
# Update all default + dev-dependencies
pdm update -d
# Update a package in the specified group of dev-dependencies
pdm update -dG test pytest
```

### 关于更新策略

同样，PDM 也提供了更新依赖关系和子依赖关系的两种不同行为，这是由 `--update<strategy>` 选项提供的。

- `reuse`：保留所有锁定的依赖关系，除了命令行中给出的依赖关系（默认）。
- `eager`：尝试锁定命令行中的软件包的较新版本以及它们的递归子依赖，并保持其他依赖的原样。

### 将软件包更新到破坏版本指定符的版本

我们可以给 `-u/--unconstrained` 来告诉 PDM 忽略 `pyproject.toml` 中的版本指定符。这与 `yarn upgrade -L/--latest` 命令的作用类似。此外，`pdm update` 也支持 `--pre/--prerelease` 选项。

## 移除已存在的依赖

要从项目文件和库目录中删除现有的依赖关系：

```bash
# Remove requests from the default dependencies
pdm remove requests
# Remove h11 from the 'web' group of optional-dependencies
pdm remove -G web h11
# Remove pytest-cov from the `test` group of dev-dependencies
pdm remove -dG test pytest-cov
```

## 安装锁定文件中的软件包

有两个类似的命令可以完成这项工作，但略有不同：

- `pdm install` 将检查锁文件，如果它与项目文件不匹配，则重新锁定，然后安装。
- `pdm sync` 在锁文件中安装依赖项，如果不存在则会出错。此外，如果给出 `--clean` 选项，`pdm sync` 也可以删除不需要的软件包。

## 用 CLI 选项选择一个依赖关系的子集

假设我们有一个项目，有以下的依赖性：

```toml
[project]  # This is production dependencies
dependencies = ["requests"]

[project.optional-dependencies]  # This is optional dependencies
extra1 = ["flask"]
extra2 = ["django"]

[tool.pdm.dev-dependencies]  # This is dev dependencies
dev1 = ["pytest"]
dev2 = ["mkdocs"]
```

| 命令                        |               功能                                           | 备注                  |
| ------------------------------- | -------------------------------------------------------------------- | ------------------------- |
| `pdm install`                   | 安装 prod 和 dev deps（没有可选）。                              |                           |
| `pdm install -G extra1`         | 安装 prod deps, dev deps 和 "extra1" 可选组               |                           |
| `pdm install -G dev1`           | 安装 prod deps，只安装 "dev1" 开发组。                         |                           |
| `pdm install -G:all`            | 安装 prod deps、dev deps 和 "extra1"、"extra2" 可选组   |                           |
| `pdm install -G extra1 -G dev1` | 安装 prod deps，"extra1" 可选组和仅 "dev1" 开发组 |                           |
| `pdm install --prod`            | 只安装 prod                                              |                           |
| `pdm install --prod -G extra1`  | 安装 prod deps 和 "extra1" 选项                              |                           |
| `pdm install --prod -G dev1`    | 失败，`--prod` 不能与 dev 依赖关系一起给定。            | 留下 `--prod` 选项 |

只要不通过 `--prod`，并且 `-G` 没有指定任何开发组，所有的开发依赖都被包括在内。

此外，如果你不希望安装根项目，可以添加 `--no-self` 选项，而 `--no-editable` 可以在你希望所有软件包以不可编辑版本安装时使用。打开 `--no-editable`，你可以安全地归档整个 `__pypackages__` 并复制到目标环境进行部署。

## 显示安装了哪些软件包

类似于 `pip list`，你可以列出软件包目录下安装的所有软件包：

```console
pdm list
```

或通过以下方式显示依赖关系图：

```
$ pdm list --graph
tempenv 0.0.0
└── click 7.0 [ required: <7.0.0,>=6.7 ]
black 19.10b0
├── appdirs 1.4.3 [ required: Any ]
├── attrs 19.3.0 [ required: >=18.1.0 ]
├── click 7.0 [ required: >=6.5 ]
├── pathspec 0.7.0 [ required: <1,>=0.6 ]
├── regex 2020.2.20 [ required: Any ]
├── toml 0.10.0 [ required: >=0.9.4 ]
└── typed-ast 1.4.1 [ required: >=1.4.0 ]
bump2version 1.0.0
```

## 设置 PyPI 索引 URL

你可以通过以下命令指定一个 PyPI 镜像 URL：

```console
pdm config pypi.url https://test.pypi.org/simple
```

默认情况下，PDM 会读取 pip 的配置文件来决定 PyPI 的 URL，如果没有找到，则回退到 `https://pypi.org/simple`，如果没有找到。

## 允许安装预先发布的版本

在 `pyproject.toml` 中包括以下设置以启用：

```toml
[tool.pdm]
allow_prereleases = true
```

## 解决锁定失败的问题

如果 PDM 不能找到满足要求的解决方案，它将引发一个错误。例如：

```bash
pdm django==3.1.4 "asgiref<3"
...
🔒 Lock failed
Unable to find a resolution for asgiref because of the following conflicts:
  asgiref<3 (from project)
  asgiref<4,>=3.2.10 (from <Candidate django 3.1.4 from https://pypi.org/simple/django/>)
To fix this, you could loosen the dependency version constraints in pyproject.toml. If that is not possible, you could also override the resolved version in [tool.pdm.overrides] table.
```

你可以改成较低版本的 `django`，或者删除 `asgiref` 的上限。但如果你的项目不符合条件。你可以通过在 `pyproject.toml` 中添加以下几行来告诉 PDM 强制将 `asgiref` 解析为一个特定的版本。

```toml
[tool.pdm.overrides]
asgiref = "3.2.10"
```

该表的每个条目都是一个带有所需版本的软件包名称。这个值也可以是一个文件或 VCS 仓库的 URL，比如 `git+https://...`。读取后，PDM 将在锁文件中钉住 `asgiref@3.2.10`，不管是否有其他可用的解决方案。

```{note}
通过使用 `[tool.pdm.overrides]` 设置，你要自己承担该决议带来的任何不兼容的风险。它只有在没有符合你要求的有效分辨率，并且你知道特定的版本可以使用时才能使用。

大多数时候，你可以把任何暂时性的约束添加到 `dependencies` 数组中。
```

## 环境变量扩展

为了方便起见，PDM 在某些情况下支持在依赖关系规范中扩展环境变量：

- URL auth 部分的环境变量将被展开：`https://${USERNAME}:${PASSWORD}/artifacts.io/Flask-1.1.2.tar.gz`。不直接给出 URL 中的 auth 部分也是可以的，当 `-v/--verbose` 开启时，PDM 会询问他们。
- `${PROJECT_ROOT}` 将以项目根的绝对路径展开，采用 POSIX 风格（即正斜杠 `/`，即使在 Windows 上也是如此）。为了保持一致性，引用 `${PROJECT_ROOT}` 下的本地路径的 URL 必须以 `file:///`（三个斜线）开始，例如 `file:///${PROJECT_ROOT}/artifacts/Flask-1.1.2.tar.gz`。

不要担心凭证泄漏，环境变量将在需要时被扩展，并在锁文件中保持不动。
