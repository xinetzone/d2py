```{post} 2023/12/14 13:55
:category: conda
:tags: FAQs
:excerpt: 1
```

# Conda 常见问题

## 修改 conda 缓存路径

只需配置文件 `~/.condarc` 即可：

```
envs_dirs:                                                                                                                                 
  - /media/pc/data/tmp/cache/conda/envs                                                                                                                              
pkgs_dirs:                                                                                                                                 
  - /media/pc/data/tmp/cache/conda/pkgs
```

## conda 解决“libstdc++.so.6: version `GLIBCXX_3.4.20‘ not found“

```bash
conda install -c anaconda libstdcxx-ng
conda install -c conda-forge gcc
```

## conda 环境下：`/lib64/libpthread.so.0` 和 `/usr/lib64/libpthread_nonshared.a ` 找不到

错误信息：
- cannot find `/usr/lib64/libpthread_nonshared.a`: No such file or directory
- cannot find `/lib64/libpthread.so.0`

这个问题是由于在创建 conda 环境时，找不到 `/lib64/libpthread.so.0` 这个文件。你可以尝试以下方法解决这个问题：

1. 首先，找到 `libpthread.so.0` 文件的位置。你可以使用 `find` 命令来查找：

```bash
sudo find / -name libpthread.so.0
```

2. 假设你找到了`libpthread.so.0`文件的路径，例如：`/usr/local/lib64/libpthread.so.0`。接下来，你需要创建一个软链接到`/lib64`目录下：

```bash
sudo ln -s /usr/local/lib64/libpthread.so.0 /lib64/libpthread.so.0
```

3. 最后，重新创建conda环境：

```bash
conda create --name your_env_name python=your_python_version
```

注意将`your_env_name`和`your_python_version`替换为你想要的环境名称和Python版本。