# Nuitka 简介

参考：

:::{card} Nuitka 文档
:link: https://nuitka.net/zh_CN/

Nuitka 将 Python 模块翻译成 C 语言程序，然后使用 `libpython` 和自己的静态 C 文件，以 CPython 的方式执行。
:::

Nuitka 的简单命令：

- `--standalone`：方便移植到其他机器，不用再安装 python。这不会输出单一的可执行文件，而是整个文件夹。将生成的 `*.dist` 文件夹复制到另一台机器上并运行它。
- `--follow-import-to=need`：`need` 为你需要编译成 C/C++ 的 python 文件夹命名
- `--show-memory --show-progress`：展示整个安装的进度过程
- `--nofollow-imports`：不编译代码中所有的 `import`（比如 `keras`，`numpy` 之类的），交给 `python3x.dll` 执行
- `--plugin-enable=qt-plugins`：用到 `pyqt5` 来做界面的，这里 `nuitka` 有其对应的插件。
- `--follow-import-to=utils,src`：需要编译成 C++ 代码的指定的 2 个包含源码的文件夹，这里用 `,` 来进行分隔。
- `--output-dir=out`：指定输出的结果路径为 `out`。
- `--windows-icon-from-ico=./logo.ico`：指定生成的 `.exe` 的图标为 `logo.ico` 这个图标，这里推荐一个将图片转成 `ico` 格式文件的网站（比特虫）。
- `--windows-disable-console`：运行 `exe` 取消弹框。
- `--onefile`: 生成单个文件。 需要 `pip install zstandard`。
- `--remove-output --no-pyi-file`: 移除构建中间产物。

::::{tip}

使用 `--standalone` 选项，需要安装一些额外的库：

```bash
conda install libpython-static
```
::::

- 指定 package： ```--include-package=PACKAGE```
- 指定 module： ```--include-module=MODULE```
- 指定目录，里面包含的所有包/模块都会被打包（覆盖其他递归选项）： ```--include-plugin-directory=MODULE/PACKAGE```
- 与 pattern 匹配的所有文件都会被打包（覆盖其他递归选项）： ```--include-plugin-files=PATTERN```

可以安装 `ordered-set` 以加速打包。ubuntu 还可以 `sudo apt install ccache`。

