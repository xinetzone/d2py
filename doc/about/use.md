# 项目使用

## 离线使用

克隆本项目后，需要配置环境：

:::{note}
使用 conda 创建并激活环境 `hs`：

```sh
conda create -n hs python=3.10
conda activate hs
```

安装 `hs` 环境的 jupyter 内核（为了方便 vscode 等编辑器使用）：

```sh
pip install ipykernel
python -m ipykernel install --user --name hs
```
:::