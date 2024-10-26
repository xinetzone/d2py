# 配置 JupyterLite 站点

一旦您初始化了一个 JupyterLite 站点，可以通过添加或编辑位于 [Lite Dir](https://jupyterlite.readthedocs.io/en/stable/reference/cli.html#the-lite-dir) 中的配置文件来更改配置。

配置值设置在 [Lite Dir](https://jupyterlite.readthedocs.io/en/stable/reference/cli.html#the-lite-dir) 中已知位置的一个或多个[运行时配置文件](https://jupyterlite.readthedocs.io/en/stable/reference/config.html)中。配置信息以级联方式合并，允许在 [Lite Dir](https://jupyterlite.readthedocs.io/en/stable/reference/cli.html#the-lite-dir) 的根目录中设置设置，并被 `repl` 和 `lab` 等单个应用程序的设置替代。

可用选项在 Jupyter Config Data [Schema](https://jupyterlite.readthedocs.io/en/stable/reference/schema-v0.html) 中定义，包括诸如 `appName`、`appVersion`、`settingsOverrides`、`exposeAppInBrowser` 等设置。

## 覆盖

除了 [Runtime Configuration Files](https://jupyterlite.readthedocs.io/en/stable/reference/config.html) 之外，还可以根据 [Customizing Settings](https://jupyterlite.readthedocs.io/en/stable/howto/configure/settings.html) 中的描述创建额外的 `overrides.json` 文件。这些文件覆盖特定的 `@jupyterlab` 设置，并合并到 jupyter 配置的 `settingsOverrides` 中。