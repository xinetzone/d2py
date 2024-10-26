# 构建钩子

编写构建钩子是相当容易的，`pdm-backend` 现在提供了 6 个钩子来定制构建过程的每一步，你不需要全部实现它们。

## 修改项目元数据

`````{tab-set}
````{tab-item} "pdm_build.py"
```python
def pdm_build_initialize(context):
    metadata = context.config.metadata
    metadata["dependencies"].append("requests")
```
````
`````

元数据可以像字典一样访问，对对象的任何更新都将立即生效。对于 sdist 构建，修改后的 `pyproject.toml` 将被写入 tarball。

```{tip}
正如你所看到的，你不需要从 `pdm.backend` 导入任何特定的东西。当然，当您希望对钩子函数进行类型注释时，可能需要这样做。
```

## 增加文件或修改收集的文件

有两种方法可以实现这一点。

1. 在 `context.build_dir` 下生成的任何文件，除非被 `excludes` 设置排除，否则将自动收集。

`````{tab-set}
````{tab-item} "pdm_build.py"
```python
def pdm_build_initialize(context):
    context.ensure_build_dir()  # make sure it is created.
    with open(os.path.join(context.build_dir, "COPYING.md"), "w") as f:  # (1)!
        f.write("This is a generated COPYING file.")
```
```{code-annotations}
1. 该文件将被打包为工件中的 `COPYING.md`。
```
````
`````



或者，可以在任何地方生成它并显式地包含路径。

`````{tab-set}
````{tab-item} "pdm_build.py"
```python
def pdm_build_update_files(context, files):
        extra_file_path = Path.home() / ".config/myconfig.yaml"
        files["myconfig.yaml"] = extra_file_path  # (1)!
```
```{code-annotations}
1. 该文件将被打包为工件中的 `myconfig.yaml`。
```
````
`````

## 调用 `setup()` 函数来构建扩展

`````{tab-set}
````{tab-item} "pyproject.toml"
```toml
[tool.pdm.build]
run-setuptools = true
```
````
````{tab-item} "pdm_build.py"
```python
from setuptools import Extension

ext_modules = [Extension("my_package.hello", ["my_package/hellomodule.c"])]

def pdm_build_update_setup_kwargs(context, setup_kwargs):
    setup_kwargs.update(ext_modules=ext_modules)
```
````
`````

## 为特定的构建目标启用钩子

有时候你只想激活特定的钩子，你可以定义 `pdm_build_hook_enabled()` 钩子：

`````{tab-set}
````{tab-item} "pdm_build.py"

```python
def pdm_build_hook_enabled(context):
    # Only enable for sdist builds
    return context.target == "sdist"
```
````
`````

你也可以查看特定钩子中的 `context` 对象来决定应该调用它。


## 构建钩子流

钩子的调用顺序如下：

```{mermaid}
flowchart TD
    A{{pdm_build_hook_enabled?}}-->pdm_build_initialize
    pdm_build_initialize-.run-setuptools.-> pdm_build_update_setup_kwargs
    pdm_build_update_setup_kwargs-.->pdm_build_update_files
    pdm_build_update_files --> pdm_build_finalize
```

## 将钩子作为插件分发

如果你想与他人共享钩子，你可以将钩子脚本文件更改为 Python 包并上传到 PyPI。

文件结构：

```
pdm-build-mypyc
├── mypyc_build.py
├── LICENSE
├── README.md
└── pyproject.toml
```

`````{tab-set}
````{tab-item} "pyproject.toml"
```toml
[build-system]
requires = ["pdm-backend"]
build-backend = "pdm.backend"

[project]
name = "pdm-build-mypyc"
version = "0.1.0"
description = "A pdm build hook to compile Python code with mypyc"
authors = [{name = "...", email = "..."}]
license = {text = "MIT"}
readme = "README.md"

[project.entry-points."pdm.build.hook"]
mypyc = "mypyc_build:MypycBuildHook"
```
```` 
````{tab-item} "mypyc_build.py"
```python
class MypycBuildHook:
    def pdm_build_hook_enabled(self, context):
        return context.target == "wheel"

    def pdm_build_initialize(self, context):
        context.ensure_build_dir()
        mypyc_build(context.build_dir)
```
````
`````

插件必须在 `pdm.build.hook` 组下发布入口点。入口点值可以是以下任意值：

- 包含钩子函数的模块
- 将钩子函数作为方法实现的类对象
- 上述类对象的实例

在它发布之后，另一个用户可以通过在 `build-system.requires` 中包含包名来启用这个钩子：

```toml
[build-system]
requires = ["pdm-backend", "pdm-build-mypyc"]
build-backend = "pdm.backend"
```
