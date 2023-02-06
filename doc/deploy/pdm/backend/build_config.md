# 构建配置

所有构建配置都存储在 `tool.pdm.build` 表下。

## 指定包目录

你可以通过设置 `package-dir` 选项告诉后端在另一个目录下查找 Python 包：

```toml
[tool.pdm.build]
package-dir = "src"
```

```{note}
缺省值：`.` （项目根），如果检测到 `src`，则为 `src`。
```

## 包括和排除文件

可以告诉后端使用 `includes` 和 `excludes` 设置从构建结果中包含其他文件或排除一些文件。每个设置都是 `glob` 模式数组，如果模式是目录名，它将被递归地包含或排除。所有相对路径都是从项目根计算的。

```toml
[tool.pdm.build]
includes = ["src", "data/*.json"]
excludes = ["*.o"]
```

### 只在 sdist 中包含文件

`source-include` 中的文件模式将仅被 sdist 包含，而被 `wheel` 和 `editable` 构建排除。

```toml
source-includes = ["tests"]
```

### 包含和排除的优先级

如果文件同时被 `includes` 和 `excludes` 覆盖，则模式中路径部分较多且通配符较少的文件胜出，否则，如果长度相同，则 `excludes` 优先。

例如，给定以下配置：

```toml
includes = ["src"]
excludes = ["**/*.json"]
```

`src/foo/data.json` 将被排除，因为 `excludes` 中的模式有更多的路径部分，但是，如果将配置更改为：

```toml
includes = ["src", "src/foo/data.json"]
excludes = ["**/*.json"]
```

相同的文件将被包含，因为它被包含在具有更特定路径的 `includes` 中。

### 默认行为

如果没有指定 `includes` 和 `excludes`，后端可以按照以下规则确定它们：

- 如果在 `package-dir` 下找到顶级包，则将包括它们以及其中的任何数据文件。
- 否则，将包括 `package-dir` 下的所有顶级 `*.py` 文件。
- 如果找到 `tests` 下的测试文件，则由 sdist 包含，并由其他格式排除。

```{note}
指定 `includes` 和 `excludes` 将覆盖默认值，因此需要手动包含包目录。`*.pyc`、`__pycache__/` 和 `build/` 总是被排除在外。
```

## 本地构建钩子

您可以指定要在构建过程之前执行的自定义脚本，该脚本可用于生成文件或修改元数据。项目根目录下名为 `pdm_build.py` 的文件将被自动检测为自定义钩子脚本，或者你可以通过自定义钩子设置指定名称：

```toml
[tool.pdm.build]
custom-hook = "build.py"
```

缺省值：`pdm_build.py`。

## 运行 setuptools

由于缺乏构建 C 扩展的能力，`pdm-backend` 允许用户从项目中自动生成 `setup.py` 调用 `setuptools`。这可以通过将 `run-setuptools` 设置为 `true` 来启用：

```toml
[tool.pdm.build]
run-setuptools = true
```

默认值：`false`。

钩子函数 `pdm_build_update_setup_kwargs` 将被调用来修改传递给 `setup()` 函数的参数。

## `is-purelib`

默认情况下，`pdm-backend` 使用标记 `py3-none-any` 生成非特定于平台的轮子。但是如果 `run-setuptools` 为真，那么构建的轮子将是特定于平台的。你可以通过显式地将 `is-purelib` 设置为 `true` 或 `false` 来覆盖这个行为：

```toml
[tool.pdm.build]
is-purelib = true
```

## 选择可编辑的构建格式

`pdm-backend` 支持两种方式来构建 {pep}`可编辑的轮子 <660>`，`path` 和 `editables`，前者是默认的。它可以通过 `editable-backend` 设置更改：

```toml
[tool.pdm.build]
editable-backend = "editables"
```

```{admonition} path
在这种方法中，可编辑的构建将非常类似于 `setuptools` 生成的遗留格式。一个包含包的父路径的 `.pth` 文件将被安装到 `site-packages` 目录中。
```

```{admonition} editables
如果选择这种方法，后端将安装代理模块，该模块将 import 语句重定向到包的实际位置，该位置由[可编辑包](https://pypi.org/project/editables)提供支持。
```

## 命令行构建选项

一些构建前端（如 [build] 和 [pdm]）支持将选项从命令行传递到后端。`pdm-backend` 支持以下选项：

- `--python-tag=<tag>` Override the python implementation compatibility tag(e.g. `cp37`, `py3`, `pp3`)
- `--py-limited-api=<abi>` Python tag (`cp32`|`cp33`|`cpNN`) for abi3 wheel tag
- `--plat-name=<plat>` Override the platform name(e.g. `win_amd64`, `manylinux2010_x86_64`)
- `no-clean-build` Don't clean the build directory before the build starts, this can also work by setting env var `PDM_BUILD_NO_CLEAN` to `1`.

例如，你可以用 [build] 来提供这些选项：

```bash
python -m build --sdist --wheel --outdir dist/ --config-setting="--python-tag=cp37" --config-setting="--plat-name=win_amd64"
```
## 环境变量

- `SOURCE_DATE_EPOCH`: Set the timestamp(seconds) of the zipinfo in the wheel for reproducible builds. The default date is 2016/01/01.

[build]: https://pypi.org/project/build
[pdm]: https://pypi.org/project/pdm