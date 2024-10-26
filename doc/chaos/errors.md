# 常见错误

- [ValueError:不能将字符串转换为浮点数](https://datascientyst.com/solve-valueerror-could-not-convert-string-to-float-pandas/)

1. ModuleNotFoundError: No module named '_curses'

```bash
pip install windows-curses
```

2. ModuleNotFoundError: No module named 'fcntl'

使用 `blessed` 替代 `blessings`：
```bash
pip uninstall blessings
pip install blessed
```

3. You indicated pty=True, but your platform doesn't support the 'pty' module!

```bash
conda install pywinpty
```

4. `jupyter` 中文乱码设置编码格式 避免控制台输出的解决

```shell
!chcp 65001
!echo 中文
```

`chcp` 可以解决此问题。
