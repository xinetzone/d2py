# 简介

PDM-Backend 是支持最新打包标准的构建后端，包括：

- {pep}`517`：构建后端 API
- {pep}`621`：项目元数据
- {pep}`660`：可编辑的构建后端

要使用它作为 {pep}`517` 构建后端，请编辑 `pyproject.toml` 如下：

```toml
[build-system]
requires = ["pdm-backend"]
build-backend = "pdm.backend"
```

在 `pyproject.toml` 中以 {pep}`621` 格式编写项目元数据：

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "A project built with PDM-Backend"
authors = [{name = "John Doe", email="me@johndoe.org"}]
dependencies = ["requests"]
requires-python = ">=3.8"
readme = "README.md"
license = {text = "MIT"}
```

然后运行 `build` 命令以 `wheel` 和 `sdist` 的形式构建项目：

```bash
pdm build
```
