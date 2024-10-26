# 从 pdm-pep517 迁移

从 [pdm-pep517] 后端迁移非常容易，两个后端配置之间只有一些不同。

## `tool.pdm.build` 表

从 1.0.0 开始 `pdm-pep517` 已重命名 `tool.pdm` 表为 `tool.pdm.build`。构建。如果您仍然将 [](./build_config.md) 直接存储在 `tool.pdm` 文件中，将它们移动到 `tool.pdm.build`。旧表不再受支持。


:::::{card-carousel} 2
::::{card} 旧式
```toml
[tool.pdm]
includes = ["src", "data/*.json"]
package-dir = "src"
```
::::
::::{card} 新式
```toml
[tool.pdm.build]
includes = ["src", "data/*.json"]
package-dir = "src"
```
::::
::::: 

## `setup-script`

在 `pdm-pep517` 中，允许在构建过程中调用自定义构建函数来添加用户生成的内容，该函数由 `tool.pdm.build.setup-script` 选项指定。但是，`pdm-backend` 中已经删除了这个选项，使用自定义钩子代替，自定义脚本可以使用名称 `pdm_build.py` 自动加载。

:::::{card-carousel} 2
::::{card} 旧式
```toml
# pyproject.toml
[tool.pdm.build]
run-setuptools = false
setup-script = "build.py"
```
```python
# build.py
def build(src, dst):
    # add more files to the dst directory
    ...
```
::::
::::{card} 新式
```toml
# pyproject.toml
[tool.pdm.build]
# Either key is not necessary anymore.
```
```python
# pdm_build.py
def pdm_build_update_files(context, files):
    # add more files to the dst directory
    new_file = do_create_files()
    files["new_file"] = new_file
```
::::
:::::

And if `run-setuptools` is `true`, `pdm-pep517` will instead generate a `setup.py` file and call the specified script to update the arguments passed to `setup()` function. In `pdm-backend`, this can be also done via custom hook:

:::::{card-carousel} 2
::::{card} 旧式

```toml
# pyproject.toml
[tool.pdm.build]
run-setuptools = true
setup-script = "build.py"
```
```python
# build.py
def build(setup_kwargs):
    # modify the setup_kwargs
    setup_kwargs['extensions'] = [Extension(...)]
```
::::
::::{card} 新式
```toml
# pyproject.toml
[tool.pdm.build]
run-setuptools = true
```
```python
# pdm_build.py
def pdm_build_update_setup_kwargs(context, setup_kwargs):
    # modify the setup_kwargs
    setup_kwargs['extensions'] = [Extension(...)]
```
::::
:::::

就这样，不需要再做任何更改，您的项目将继续像以前一样工作。