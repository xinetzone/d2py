# 管理依赖

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

更多待更：[依赖](https://pdm.fming.dev/usage/dependency/)