# Python 编译器 Nuitka

参考：

- [官方教程中文版](https://daobook.github.io/nuitka-doc/zh_CN/)
- [Nuitka常见问题解决集锦-独孤九剑之破Bug式](https://zhuanlan.zhihu.com/p/156883484)

Nuitka 将 Python 模块翻译成 C 级程序，然后使用 `libpython` 和自己的静态 C 文件，以 CPython 的方式执行。

Nuitka 的简单命令：

- `--standalone`：方便移植到其他机器，不用再安装 python
- `--follow-import-to=need`：`need` 为你需要编译成 C/C++ 的 python 文件夹命名
- `--show-memory --show-progress`：展示整个安装的进度过程
- `--nofollow-imports`：不编译代码中所有的 `import`（比如 `keras`，`numpy` 之类的），交给 `python3x.dll` 执行
- `--plugin-enable=qt-plugins`：用到 `pyqt5` 来做界面的，这里 `nuitka` 有其对应的插件。
- `--follow-import-to=utils,src`：需要编译成 C++ 代码的指定的 2 个包含源码的文件夹，这里用 `,` 来进行分隔。
- `--output-dir=out`：指定输出的结果路径为 `out`。
- `--windows-icon-from-ico=./logo.ico`：指定生成的 `.exe` 的图标为 `logo.ico` 这个图标，这里推荐一个将图片转成 `ico` 格式文件的网站（比特虫）。
- `--windows-disable-console`：运行 `exe` 取消弹框。
