```{post} 2021/11/10 18:00
:category: Python
:tags: basic, udata
:excerpt: 1
```

# 恒有数 Python 接口

[恒有数](https://udata.hs.net/home?channel_source=vnpy) 提供了大量金融数据相关的接口，借助此平台讲解 Python 基础知识。

支持平台：

1. Window10 或者更高版本的系统平台
2. Ubuntu20.04 或者更高版本

后续的教程均指代 Python 为 Python3.10。

## 配置 `conda` 环境

使用 conda 创建并激活环境 `hs`：

```sh
conda create -n hs python=3.10
conda activate hs
```

安装 `hs` 环境的 jupyter 内核（为了方便 vscode 等编辑器使用）：

```sh
conda install ipykernel
python -m ipykernel install --user --name hs
```

## 安装 Jupyter 插件

参考：https://github.com/ipython-contrib/jupyter_contrib_nbextensions

安装插件：

```sh
pip install jupyter_contrib_nbextensions
```

安装 javascript 和 css 文件：

```sh
jupyter contrib nbextension install --user
```

安装代码格式化工具：

```sh
pip install autopep8
```

## 安装**恒有数**的相关包

```{warning}
需要配置 `conda` 环境 {guilabel}`hs`。
```

1. 在恒有数[主页](https://udata.hs.net) 完成注册登录，可用手机号或微信进行注册登录；
2. 使用 `pip` 安装需要的包（文件在 {download}`pip-env/hs_udata.txt <../../pip-env/hs_udata.txt>`）：

```sh
cd docs
pip install -r pip-env/hs_udata.txt
```

祝贺，全部的准备工作完成了！
