# 在 GitHub Pages 上部署你的第一个 JupyterLite 网站

```{hint}
如果你首先想熟悉界面，请查看 [用户指南](./using.md)。
```

JupyterLite 可以轻松地部署在 [GitHub Pages] 上，使用 `jupyter-lite` CLI 添加内容和扩展。

```{note}
部署到 GitHub Pages 需要 Github 账户。
```

## 从模板生成新仓库

[jupyterlite demo] 仓库是模板，可以方便地：

- 使用预构建的 JupyterLite 构建 JupyterLite 网站，将一系列现有的 Jupyter Notebook 作为分发的一部分
- 将网站部署到 GitHub Pages

这个过程使用 Github Actions 自动化。

点击 "Use this template"（使用此模板）以从此模板生成你自己的仓库：

![动画 gif，展示了如何使用提供的仓库模板来生成新网站。](https://user-images.githubusercontent.com/21197331/125816904-5768008a-77de-4cb3-8013-f3999b135c02.gif)

从你的仓库的 _Actions_ 标签页中，确保工作流是启用的。当你向 `main` 分支提交一个 commit 时，一个 Github Action 将会构建你的 JupyterLite 版本并将其部署到仓库的 Github Pages。默认情况下，Github Pages 网站可以在 `YOUR_GITHUB_USERNAME.github.io/YOUR_REPOSITORY-NAME` 找到。你也可以从仓库的 _Settings_ 标签页中的 _Pages_ 菜单项检查 URL。

如果部署失败，请前往 "设置 - Actions - General"，在 "工作流权限" 部分，检查 "读取和写入权限"。检查你是否为你的仓库启用了 Github Pages：从你的仓库 _设置_ 标签页中，选择 _页面_ 菜单项，并确保源设置为 `GitHub Actions`。

![一个截图，显示了用于部署到 GitHub Pages 的 GitHub Actions 配置选项。](https://user-images.githubusercontent.com/591645/183384744-d7e08150-8f5f-4a50-bd53-5c99b1fd99a1.png)

当你提交一个文件时，一个更新后的网站将被构建并发布在 Github Pages 上。

```{note}
请注意，Github Pages 网站更新可能需要几分钟时间。在你的网络浏览器中对你的 Github Pages 网站进行强制刷新以查看网站的新版本。
```

```{note}
或者，你可以使用 [JupyterLite demo using xeus-python] 来在 Github Pages 上发布一个默认使用 xeus-python 的部署，并允许使用 ``emscripten-forge`` 和 ``conda-forge`` 预安装软件包。
```

## 访问 JupyterLite 网站

构建完成后，网站将在 GitHub Pages 上可用。前往 `https://YOUR_GITHUB_USERNAME.github.io/YOUR_REPOSITORY-NAME` 以访问它：

![在 GitHub Pages 上使用 JupyterLite 网站的动画屏幕录像。](https://user-images.githubusercontent.com/591645/120649478-18258400-c47d-11eb-80e5-185e52ff2702.gif)

```{note}
默认情况下，由 `jupyterlite/demo` 仓库提供的部署包括一个 `.nojekyll` 文件，以绕过 GitHub Pages 上的 Jekyll 处理。

有关更多信息，请参阅这篇 [博客文章](https://github.blog/2009-12-29-bypassing-jekyll-on-github-pages/)。
```

## 部署新版本的 JupyterLite

要更改预构建的 JupyterLite 资产的版本，更新 `requirements.txt` 文件中的 `jupyterlite-core` 包版本。

提交并推送更改。网站将在下一次推送到 `main` 分支时被部署。

## 向部署中添加额外要求

````{note}
[jupyterlite/demo](https://github.com/jupyterlite/demo) 仓库使用 `requirements.txt` 文件来指定依赖项。出于演示目的，此文件可能包含您希望从部署中移除的额外内核和扩展。如果是这种情况，您可以坚持使用更简化的 `requirements.txt` 文件，例如：

```bash
# 用于构建 JupyterLite 网站的核心包
jupyterlite-core==0.1.0b19
# 由 Pyodide 提供支持的 Python 内核
jupyterlite-pyodide-kernel==0.0.5
# 内容索引的依赖项
jupyterlab~=3.5.3
```
````

### 扩展

`requirements.txt` 文件可用于向部署的 JupyterLite 网站添加额外的预构建（也称为 _federated_ ）JupyterLab 扩展。遵循 [扩展指南](https://jupyterlite.readthedocs.io/en/stable/howto/configure/simple_extensions.html) 了解更多信息。

### 使用 xeus-python 内核和 emscripten-forge

使用 [带有 xeus-python 的 JupyterLite 部署](https://github.com/jupyterlite/xeus-python-demo)，您可以通过在 `environment.yml` 文件中指定它们，预先安装 `conda-forge` 和 `emscripten-forge` 上可用的包。

通过预安装包，它们可以在内核中立即使用，并且无需 `piplite` 即可导入。

### 内容

您可以通过点击 `contents` 目录并将桌面上的笔记本拖放到内容列表中，来添加和更新默认笔记本和文件。等待文件上传完成，然后保存它们（提交到仓库的 `main` 分支）。

查看有关 [管理内容](https://jupyterlite.readthedocs.io/en/stable/howto/content/files.html) 的指南以了解更多信息。

## 更多信息

如果您想自定义您的 JupyterLite 网站，请查看不同的 [操作指南](https://jupyterlite.readthedocs.io/en/stable/howto/)。

[jupyterlite demo]: https://github.com/jupyterlite/demo
[github pages]: https://pages.github.com/
