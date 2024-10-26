# 管理项目

PDM 可以作为 {pep}`517` 的构建后端，要启用它，请在你的 `pyproject.toml`。如果你用 `pdm init` 为你创建它，应该已经完成了。

```toml
[build-system]
requires = ["pdm-pep517"]
build-backend = "pdm.pep517.api"
```

`pip` 将读取后台设置来安装或构建软件包。

(pdm:choose-a-python-interpreter)=
## 选择 Python 解释器

如果你使用过 `pdm init`，你一定已经看到了 PDM 是如何检测和选择 Python 解释器。在初始化之后，你也可以通过 `pdm use <python_version_or_path>` 来改变设置。参数可以是任何长度的版本说明，也可以是相对或绝对的路径，指向相对或绝对路径，但请记住，Python 解释器必须符合项目文件中的 `requires-python` 的约束。

```{admonition} 应用程序或库
您可能已经注意到，PDM 会询问您该项目是否是要上传到 PyPI 的库。[这里](https://pipenv.pypa.io/en/latest/advanced/#pipfile-vs-setup-py) 有很好的解释它们之间的区别。PDM 通过检查 `pyproject.toml` 中的 `project.name` 字段知道这一点。如果它不是空的，它将被认为是一个库。库可以通过 `pdm build` 或其他 {pep}`517` 构建器构建，并且每次执行 `pdm sync` 或 `pdm install` 时，库本身将以可编辑模式安装，除非使用 `--no-self` 选项选择退出。相反，应用程序不能安装，因为它缺少项目 `name`。
```

### `requires-python` 如何控制项目

PDM 尊重 `requires-python` 的值，它试图挑选能够在 `requires-python` 包含的所有 python 版本上工作的候选包。在所有 `requires-python` 包含的 python 版本上工作。例如，如果 `requires-python` 是 `>=2.7`，PDM 将尝试找到最新版本的 `foo`，其 `requires-python` 的版本范围是 `>=2.7` 的 **superset**。

因此，如果你不希望任何过时的软件包被锁定，请确保你正确地编写 `requires-python`。

### Working with Python < 3.7

Although PDM run on Python 3.7 and above, you can still have lower Python versions for your **working project**. But remember, if your project is a library, which needs to be built, published or installed, you make sure the PEP 517 build backend being used supports the lowest Python version you need. For instance, the default backend `pdm-pep517` only works on Python 3.7+, so if you run `pdm build` on a project with Python 3.6, you will get an error. Most modern build backends have dropped the support for Python 3.6 and lower, so it is highly recommended to upgrade the Python version to 3.7+. Here are the supported Python range for some commonly used build backends, we only list those that support PEP 621 since otherwise PDM can't work with them.

| Backend               | Supported Python | Support PEP 621 |
| --------------------- | ---------------- | --------------- |
| `pdm-pep517`          | `>=3.7`          | Yes             |
| `setuptools>=60`      | `>=3.7`          | Experimental    |
| `hatchling`           | `>=3.7`          | Yes             |
| `flit-core>=3.4`      | `>=3.6`          | Yes             |
| `flit-core>=3.2,<3.4` | `>=3.4`          | Yes             |

Note that if your project is an application(without `name` metadata), the above limitation of backends don't apply, since you don't need a build backend after all, and you can use a Python version up to `2.7`.

## 构建分发工件

```console
$ pdm build
- Building sdist...
- Built pdm-test-0.0.0.tar.gz
- Building wheel...
- Built pdm_test-0.0.0-py3-none-any.whl
```

然后可以通过 [twine](https://pypi.org/project/twine) 或使用 [pdm-publish](https://github.com/branchvincent/pdm-publish) 插件将工件上传至 PyPI。可用的选项可以通过输入 `pdm build --help` 即可找到可用的选项。

## 显示当前的 Python 环境

```console
$ pdm info
Python Interpreter: D:/Programs/Python/Python38/python.exe (3.8.0)
Project Root:       D:/Workspace/pdm
                                                                                                                                   [10:42]
$ pdm info --env
{
  "implementation_name": "cpython",
  "implementation_version": "3.8.0",
  "os_name": "nt",
  "platform_machine": "AMD64",
  "platform_release": "10",
  "platform_system": "Windows",
  "platform_version": "10.0.18362",
  "python_full_version": "3.8.0",
  "platform_python_implementaiton": "CPython",
  "python_version": "3.8",
  "sys_platform": "win32"
}
```

[`pdm info`](https://pdm.fming.dev/latest/usage/cli_reference/#exec-0--info) 命令用于检查项目正在使用哪种模式：

- 如果 `Project Packages` 为 `None`，则启用 [virtualenv 模式](https://pdm.fming.dev/latest/usage/venv/)。
- 否则，启用 [PEP 582 模式](pep582)。

## 配置项目

PDM 的 `config` 命令与 `git config` 的工作方式一样，只是不需要 `--list` 来显示配置。

显示当前的配置：

```console
pdm config
```

获得一个单一的配置：

```console
pdm config pypi.url
```

改变配置值并存储在主配置中：

```console
pdm config pypi.url "https://test.pypi.org/simple"
```

默认情况下，配置是全局性的，如果你想让配置只被这个项目看到，可以添加一个 `--local` 标志：

```console
pdm config --local pypi.url "https://test.pypi.org/simple"
```

任何本地配置将被存储在项目根目录下的 `.pdm.toml` 中。

配置文件按以下顺序进行搜索：

1. `<PROJECT_ROOT>/.pdm.toml` - project 配置
2. `<CONFIG_ROOT>/config.toml` - home 配置
3. `<SITE_CONFIG_ROOT>/config.toml` - site 配置

```{note}
这里 `<CONFIG_ROOT>`：

- `$XDG_CONFIG_HOME/pdm` (大部分情况下位于 `~/.config/pdm`) 在 Linux 上由 [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html) 定义
- `~/Library/Preferences/pdm` 在 MacOS 上由 [Apple File System Basics](https://developer.apple.com/library/archive/documentation/FileManagement/Conceptual/FileSystemProgrammingGuide/FileSystemOverview/FileSystemOverview.html) 定义
- `%USERPROFILE%\AppData\Local\pdm` 在 Windows 上由 [Known folders](https://docs.microsoft.com/en-us/windows/win32/shell/known-folders) 定义

且 `<SITE_CONFIG_ROOT>` 是：

- `$XDG_CONFIG_DIRS/pdm` (大部分情况下位于 `/etc/xdg/pdm`) 在 Linux 上由 [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html) 定义
- `/Library/Preferences/pdm` 在 MacOS 上由 [Apple File System Basics](https://developer.apple.com/library/archive/documentation/FileManagement/Conceptual/FileSystemProgrammingGuide/FileSystemOverview/FileSystemOverview.html) 定义
- `C:\ProgramData\pdm\pdm` 在 Windows 上由 [Known folders](https://docs.microsoft.com/en-us/windows/win32/shell/known-folders) 定义
```

如果使用 `-g/--global` 选项，第一项将被  `<CONFIG_ROOT>/global-project/.pdm.toml` 替换。

你可以在 [配置页](configuration) 中找到所有可用的配置项目。

## 配置 PyPI 索引

从 PDM 2.4.0 开始，在配置文件中支持多个 PyPI 索引。要添加新的索引，需要在配置文件中包含以下内容：

```toml
[pypi.extra]
url = "https://extra.pypi.org/simple"
verify_ssl = false
```

可用选项：

- `url`: index 的 URL
- `verify_ssl`: (可选)是否验证 SSL 证书，默认为 `true`
- `username`: (可选)索引的用户名
- `password`: (可选)索引密码
- `type`: (可选) `index` 或 `find_links`，默认为 `index`

要配置 **main** 索引，请省略索引的名称：

```toml
[pypi]
url = "https://pypi.org/simple"
verify_ssl = true
```

索引配置也可以通过 `pdm config` 命令检索或更新：

```bash
# Get the url of the index named "extra"
pdm config pypi.extra.url
# Set the username and password of the index named "extra"
pdm config pypi.extra.username "foo"
pdm config pypi.extra.password "password4foo"
```

```{note}
配置的索引将在 `pyproject.toml` 中的源代码之后尝试，如果您想完全忽略本地配置的索引，包括主索引，请设置配置值 `pypi.ignore_stored_index` 为 `False`，并且 `pyproject.toml` 中只有 sources 会很荣幸的。
```

## 将项目发布到 PyPI

使用 PDM，您可以一步构建项目并将其上传到 PyPI。

```bash
pdm publish
```

您可以指定您想要发布的存储库：

```bash
pdm publish -r pypi
```

PDM 将从配置中查找名为 `pypi` 的存储库，并使用 URL 进行上传。你也可以用 `-r/--repository` 选项直接给出 URL：

```bash
pdm publish -r https://test.pypi.org/simple
```

通过输入 `pdm publish --help` 查看所有支持的选项。

### 为上传配置存储库密钥

当使用 `pdm publish` 命令时，它从 *global* 配置文件（`<CONFIG_ROOT>/config.toml`）中读取存储库密钥。配置的内容如下：

```toml
[repository.pypi]
username = "frostming"
password = "<secret>"

[repository.company]
url = "https://pypi.company.org/legacy/"
username = "frostming"
password = "<secret>"
ca_certs = "/path/to/custom-cacerts.pem"
```

PEM-编码的证书颁发机构包(`ca_certs`)可用于本地/自定义 PyPI 存储库，其中服务器证书不是由标准 [certifi](https://github.com/certifi/python-certifi/blob/master/certifi/cacert.pem) CA 包签名的。

```{note}
存储库不同于前一节中的索引。存储库用于发布，而索引用于锁定和解析。它们没有共享配置。
```

```{tip}
您不需要为 `pypi` 和 `testpypi` 存储库配置 `url`，它们由默认值填充。用户名、密码和证书颁发机构包可以分别通过 `--username`、`--password` 和 `--ca-certs` 从 `pdm publish` 的命令传递进来。
```

要从命令行更改存储库配置，使用 `pdm config` 命令：

```bash
pdm config repository.pypi.username "__token__"
pdm config repository.pypi.password "my-pypi-token"

pdm config repository.company.url "https://pypi.company.org/legacy/"
pdm config repository.company.ca_certs "/path/to/custom-cacerts.pem"
```

## 缓存轮子的安装

如果软件包被系统中的许多项目所需要，每个项目都必须保留自己的副本。这可能会造成磁盘空间的浪费，特别是对于数据科学和机器学习库。

PDM 支持 _缓存_ 同一轮子的安装，将其安装到集中的包/库，并在不同的项目中链接到该安装。要启用它，请运行：

```bash
pdm config install.cache on
```

它可以以项目为单位，通过在命令中添加 `--local` 选项来启用。

缓存位于 `$(pdm config cache_dir)/packages` 下。人们可以通过 `pdm cache info` 查看缓存的使用情况。但是请注意，缓存的安装是自动管理的 -- 当不与任何项目连接时，它们会被删除。手动删除磁盘中的缓存可能会破坏系统中的一些项目。

```{note}
只有从 PyPI 解决的命名的 requirements 的安装可以被缓存。
```

## 管理全局项目

有时，用户可能也想跟踪全局 Python 解释器的依赖关系。通过大多数子命令支持的 `-g/--global` 选项，用 PDM 很容易做到这一点。

如果通过该选项，`<CONFIG_ROOT>/global-project` 将被用作项目目录，除了 `pyproject.toml` 会自动为你创建，并且不支持构建功能外，几乎与普通项目相同。这个想法来自 Haskell 的[stack](https://docs.haskellstack.org)。

然而，与 `stack` 不同，默认情况下，如果没有找到本地项目，PDM 不会自动使用全局项目。用户应该明确传递 `-g/--global` 来激活它，因为如果软件包进入了错误的地方，这不是很令人高兴。但 PDM 也把决定权留给用户，只要把配置 `global_project.fallback` 设为 `true` 即可。

默认情况下，当 PDM 隐式使用全局项目时，打印以下消息：项目未找到，退回到全局项目。要禁用此消息，请设置 `global_project.fallback_verbose` 设为 `false`。

如果你想让全局项目跟踪除 `<CONFIG_ROOT>/global-project` 以外的另一个项目文件，你可以通过 `-p/--project <path>` 选项提供项目路径。

```{caution}
在使用全局项目时，要小心使用 `remove` 和 `sync --clean` 命令，因为它可能会删除你的系统 Python 中安装的软件包。
```

## 从现有项目文件中导入项目元数据

如果你已经是其他软件包管理工具，如 Pipenv 或 Poetry，很容易迁移到 PDM。PDM 提供了 `import` 命令，这样你就不必手动初始化项目了，它现在支持：

1. Pipenv 的 `Pipfile`
2. Poetry 的部分在 `pyproject.toml`
3. Flit 的部分在 `pyproject.toml`
4. Pip 格式的 `requirements.txt`
5. setuptools `setup.py`(It requires `setuptools` to be installed in the project environment. You can do this by configuring `venv.with_pip` to `true` for venv and `pdm add setuptools` for `__pypackages__`)

此外，在执行 `pdm init` 或 `pdm install` 时，如果您的 PDM 项目尚未初始化，PDM 可以自动检测要导入的可能文件。

```{caution}
转换 `setup.py` 将使用项目解释器执行该文件。确保 `setuptools` 与解释器一起安装，并且 `setup.py` 是受信任的。
```

## 将锁定的软件包导出为其他格式

你也可以将 `pdm.lock` 导出为其他格式，以简化 CI 流程或镜像构建过程。目前。只有 `requirements.txt` 和 `setup.py` 格式被支持。

```console
pdm export -o requirements.txt
pdm export -f setuppy -o setup.py
```

## 使用版本控制

你 **必须** 提交 `pyproject.toml` 文件。您 **应该** 提交 `pdm.lock` 文件。不要提交 `.pdm.toml` 文件。

`pyproject.toml` 文件必须提交，因为它包含项目的构建元数据和 PDM 所需的依赖项。它也通常被其他 python 工具用于配置。关于 `pyproject.toml` 可以阅读 [pip.pypa.io/en/stable/reference/build-system/pyproject-toml/](https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/)。

您应该提交 `pdm.lock` 文件，这样做可以确保所有安装程序都使用相同版本的依赖项。要了解如何更新依赖项，请参阅[更新现有依赖项](pdm:update-existing-dependencies)。

没有必要提交 `.pdm.toml` 文件，因为它包含特定于您的系统的配置。如果你正在使用 git，你可以安全地添加 `.pdm.toml` 到你的 `.gitignore` 文件。

## 从 `pyproject.toml` 中隐藏凭证

有很多时候，需要使用敏感信息，例如 PyPI 服务器的登录凭证 和 VCS 仓库的用户名密码。不想在 `pyproject.toml` 中暴露这些信息并将其上传到 git。

PDM 提供了几种方法来实现这一点：

1. 用户可以通过环境变量给出认证信息，这些变量直接在 URL 中编码：

   ```toml
   [[tool.pdm.source]]
   url = "http://${INDEX_USER}:${INDEX_PASSWD}@test.pypi.org/simple"
   name = "test"
   verify_ssl = false

   [project]
   dependencies = [
     "mypackage @ git+http://${VCS_USER}:${VCS_PASSWD}@test.git.com/test/mypackage.git@master"
   ]
   ```

   环境变量必须以 `${ENV_NAME}` 的形式编码，其他形式不支持。此外，只有 auth 部分会被展开。

2. 如果 URL 中没有提供证书，并且从服务器收到 401 响应，当 `-v/--verbose` 作为命令行参数时，PDM 将提示用户名和密码。作为命令行参数时，PDM 将提示用户名和密码，否则 PDM 将失败，并告诉用户发生了什么。然后用户可以选择在确认问题后将证书存储在 keyring 中。

3. VCS 存储库只应用第一种方法，而索引服务器则同时应用两种方法。

## 管理缓存

PDM 提供了方便的命令组来管理缓存，有四种缓存：

1. `wheels/` 存储非轮子分布和文件的构建结果。
1. `http/` 存储 HTTP 响应内容。
1. `metadata/` 存储由解析器检索的包元数据。
1. `hashes/` 存储从软件包索引中获取的或本地计算的文件散列值。
1. `packages/` 已安装的轮子的中心化储存库。

通过输入 `pdm cache info` 查看当前的缓存使用情况。此外，你可以使用 `add`、`remove` 和 `list` 子命令来管理缓存内容。
通过每个命令的 `--help` 选项查找用法。
