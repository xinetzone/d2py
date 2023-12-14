```{post} 2023/12/14 13:55
:category: GitHub
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
