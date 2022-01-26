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

| Command                         | What it does                                                         | Comments                  |
| ------------------------------- | -------------------------------------------------------------------- | ------------------------- |
| `pdm install`                   | install prod and dev deps (no optional)                              |                           |
| `pdm install -G extra1`         | install prod deps, dev deps, and "extra1" optional group             |                           |
| `pdm install -G dev1`           | install prod deps and only "dev1" dev group                          |                           |
| `pdm install -G:all`            | install prod deps, dev deps and "extra1", "extra2" optional groups   |                           |
| `pdm install -G extra1 -G dev1` | install prod deps, "extra1" optional group and only "dev1" dev group |                           |
| `pdm install --prod`            | install prod only                                                    |                           |
| `pdm install --prod -G extra1`  | install prod deps and "extra1" optional                              |                           |
| `pdm install --prod -G dev1`    | Fail, `--prod` can't be given with dev dependencies                  | Leave the `--prod` option |

**All** development dependencies are included as long as `--prod` is not passed and `-G` doesn't specify any dev groups.

Besides, if you don't want the root project to be installed, add `--no-self` option, and `--no-editable` can be used when you want all packages to be installed in non-editable versions. With `--no-editable` turn on, you can safely archive the whole `__pypackages__` and copy it to the target environment for deployment.

## Show what packages are installed

Similar to `pip list`, you can list all packages installed in the packages directory:

```console
pdm list
```

Or show a dependency graph by:

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

## Set PyPI index URL

You can specify a PyPI mirror URL by following commands:

```console
pdm config pypi.url https://test.pypi.org/simple
```

By default, PDM will read the pip's configuration files to decide the PyPI URL, and fallback
to `https://pypi.org/simple` if none is found.

## Allow prerelease versions to be installed

Include the following setting in `pyproject.toml` to enable:

```toml
[tool.pdm]
allow_prereleases = true
```

## Solve the locking failure

If PDM is not able to find a resolution to satisfy the requirements, it will raise an error. For example,

```bash
pdm django==3.1.4 "asgiref<3"
...
🔒 Lock failed
Unable to find a resolution for asgiref because of the following conflicts:
  asgiref<3 (from project)
  asgiref<4,>=3.2.10 (from <Candidate django 3.1.4 from https://pypi.org/simple/django/>)
To fix this, you could loosen the dependency version constraints in pyproject.toml. If that is not possible, you could also override the resolved version in [tool.pdm.overrides] table.
```

You can either change to a lower version of `django` or remove the upper bound of `asgiref`. But if it is not eligible for your project,
you can tell PDM to forcedly resolve `asgiref` to a specific version by adding the following lines to `pyproject.toml`:

_New in version 1.12.0_

```toml
[tool.pdm.overrides]
asgiref = "3.2.10"
```
Each entry of that table is a package name with the wanted version. The value can also be a URL to a file or a VCS repository like `git+https://...`.
On reading this, PDM will pin `asgiref@3.2.10` in the lock file no matter whether there is any other resolution available.

!!! NOTE
    By using `[tool.pdm.overrides]` setting, you are at your own risk of any incompatibilities from that resolution. It can only be
    used if there is no valid resolution for your requirements and you know the specific version works.
    Most of the time, you can just add any transient constraints to the `dependencies` array.

## Environment variables expansion

For convenience, PDM supports environment variables expansion in the dependency specification under some circumstances:

- Environment variables in the URL auth part will be expanded: `https://${USERNAME}:${PASSWORD}/artifacts.io/Flask-1.1.2.tar.gz`.
  It is also okay to not give the auth part in the URL directly, PDM will ask for them when `-v/--verbose` is on.
- `${PROJECT_ROOT}` will be expanded with the absolute path of the project root, in POSIX style(i.e. forward slash `/`, even on Windows).
  For consistency, URLs that refer to a local path under `${PROJECT_ROOT}` must start with `file:///`(three slashes), e.g.
  `file:///${PROJECT_ROOT}/artifacts/Flask-1.1.2.tar.gz`.

Don't worry about credential leakage, the environment variables will be expanded when needed and kept untouched in the lock file.
