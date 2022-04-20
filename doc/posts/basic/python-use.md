```{post} Nov 03, 2021 23:00
:category: Python
:tags: basic
:excerpt: 1
```

# 如何使用 Python？

本站默认 Python 为 Python3。

首先，观看视频：

1. [从零搭建 AI 环境](https://www.zhihu.com/zvideo/1423062760733700096)
2. [如何使用 vscode 管理资源 & GitHub 简单介绍](https://www.zhihu.com/zvideo/1434638185800708096)

支持 Window 和 Ubuntu 搭建 AI 环境。

## 如何安装 Python 包？

主要介绍如何使用 `conda` 与 `pip` 管理环境和包。

### 创建环境：

```sh
conda create -n ai python=3.10
```

此命令表示：基于 `Python3.10` 创建名为 `ai` 的 Python 环境。

### 安装包

安装包有两种方法：

1. `pip install 包名称`（这里的 `包名称` 可以是 `.whl` 网址或者 `git` 网址）
2. `conda install 包名称`

### 卸载包

有两种方法：

1. `pip uninstall 包名称`
2. `conda uninstall 包名称`

### 更新包

有两种方法：

1. `pip install --upgrade 包名称`
2. `conda update 包名称`

### 查看环境列表

```sh
conda env list
```

### 激活/失活环境

激活：

```sh
conda activate 环境名称
```

失活：

```sh
conda deactivate
```

### 删除环境

```sh
conda remove -n 环境名称 --all
```

{guilabel}`本节视频`

<iframe id="Python"
    title="如何使用 Python？"
    width="100%"
    height="500"
    src="https://developer.hs.net/thread/1532?nav=course">
</iframe>

