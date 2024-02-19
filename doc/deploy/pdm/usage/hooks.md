# 生命周期和钩子

与任何 Python deliverable 一样，您的项目将经历 Python 项目生命周期的不同阶段，PDM 提供命令来执行这些阶段的预期任务。

它还提供了附加到这些步骤的钩子，允许：

- 插件监听同名的 [signals][pdm.signals]。
- 开发人员定义具有相同名称的自定义脚本。

内置命令目前分为 3 组：

- 1. [初始化阶段](pdm-hooks:initialization)
- 2. [依赖管理](pdm-hooks:dependencies-management)
- 3. [发布阶段](pdm-hooks:publication)

您很可能需要在安装和发布阶段之间执行一些循环任务（内务管理、检测、测试……），这就是为什么 PDM 允许您使用[用户脚本](pdm:user-scripts)定义自己的任务/阶段。

为了提供充分的灵活性，PDM 允许按需[跳过](pdm-hooks:skipping)一些挂钩和任务。

(pdm-hooks:initialization)=
## 初始化

初始化阶段应该在项目生命周期中只发生一次，通过运行 `pdm init` 命令来初始化现有项目(提示填充 `pyproject.toml` 文件)。

它们会触发以下钩子：

- [`post_init`](https://pdm.fming.dev/latest/plugin/reference/#pdm.signals.post_init)

```{mermaid}
flowchart LR
  subgraph pdm-init [pdm init]
    direction LR
    post-init{{Emit post_init}}
    init --> post-init
  end
```

(pdm-hooks:dependencies-management)=
## 依赖管理

依赖关系管理是开发人员能够工作和执行以下工作所必需的：

- `lock`：根据 `pyproject.toml` 需求计算锁文件。
- `sync`：从锁定文件中同步(添加/删除/更新) {pep}`582` 包，并将当前项目安装为可编辑的。
- `add`：添加依赖
- `remove`：删除依赖

所有这些步骤都可以直接使用以下命令：

- [`pdm lock`](https://pdm.fming.dev/latest/usage/cli_reference/#exec-0--lock): execute the `lock` task
- [`pdm sync`](https://pdm.fming.dev/latest/usage/cli_reference.md#exec-0--sync): execute the `sync` task
- [`pdm install`](https://pdm.fming.dev/latest/usage/cli_reference.md#exec-0--install): execute the `sync` task, preceded from `lock` if required
- [`pdm add`](https://pdm.fming.dev/latest/usage/cli_reference.md#exec-0--add): add a dependency requirement, re-lock and then sync
- [`pdm remove`](https://pdm.fming.dev/latest/usage/cli_reference.md#exec-0--remove): remove a dependency requirement, re-lock and then sync
- [`pdm update`](https://pdm.fming.dev/latest/usage/cli_reference.md#exec-0--update): re-lock dependencies from their latest versions and then sync

会触发如下钩子：

- [`pre_install`](https://pdm.fming.dev/latest/plugin/reference/#pdm.signals.pre_install#pdm.signals.pre_install)
- [`post_install`](https://pdm.fming.dev/latest/plugin/reference/#pdm.signals.pre_install#pdm.signals.post_install)
- [`pre_lock`](https://pdm.fming.dev/latest/plugin/reference/#pdm.signals.pre_install#pdm.signals.pre_lock)
- [`post_lock`](https://pdm.fming.dev/latest/plugin/reference/#pdm.signals.pre_install#pdm.signals.post_lock)

```{mermaid}
flowchart LR
  subgraph pdm-install [pdm install]
    direction LR

    subgraph pdm-lock [pdm lock]
      direction TB
      pre-lock{{Emit pre_lock}}
      post-lock{{Emit post_lock}}
      pre-lock --> lock --> post-lock
    end

    subgraph pdm-sync [pdm sync]
      direction TB
      pre-install{{Emit pre_install}}
      post-install{{Emit post_install}}
      pre-install --> sync --> post-install
    end

    pdm-lock --> pdm-sync
  end
```

### 切换 Python 版本

这是依赖项管理中的特殊情况：您可以使用 `pdm use` 切换当前 Python 版本，它将使用新的 Python 解释器发出 [`post_use`](https://pdm.fming.dev/latest/plugin/reference/#pdm.signals.post_use) 信号。

```{mermaid}
flowchart LR
  subgraph pdm-use [pdm use]
    direction LR
    post-use{{Emit post_use}}
    use --> post-use
  end
```


(pdm-hooks:publication)=
## 发布

一旦准备好发布的包/库，将需要发布任务：

- [`build`](https://pdm.fming.dev/latest/usage/cli_reference/#exec-0--build)：构建/编译需要它的资产，并将所有内容打包到 Python 包中（sdist, wheel）
- [`upload`](https://pdm.fming.dev/latest/usage/cli_reference/#exec-0--publish)：上传/发布包到远程 PyPI 索引

会触发：

- [`pre_publish`](https://pdm.fming.dev/latest/plugin/reference/#pdm.signals.pre_publish)
- [`post_publish`](https://pdm.fming.dev/latest/plugin/reference/#pdm.signals.post_publish)
- [`pre_build`](https://pdm.fming.dev/latest/plugin/reference/#pdm.signals.pre_build)
- [`post_build`](https://pdm.fming.dev/latest/plugin/reference/#pdm.signals.post_build)


```{mermaid}
flowchart LR
  subgraph pdm-publish [pdm publish]
    direction LR
    pre-publish{{Emit pre_publish}}
    post-publish{{Emit post_publish}}

    subgraph pdm-build [pdm build]
      pre-build{{Emit pre_build}}
      post-build{{Emit post_build}}
      pre-build --> build --> post-build
    end

    %% subgraph pdm-upload [pdm upload]
    %%   pre-upload{{Emit pre_upload}}
    %%   post-upload{{Emit post_upload}}
    %%   pre-upload --> upload --> post-upload
    %% end

    pre-publish --> pdm-build --> upload --> post-publish
  end
```

执行将在第一次失败时停止，包括钩子。

(pdm:user-scripts)=
## 用户脚本

[用户脚本](scripts.md) 部分中有详细说明，但你应该知道：

- 每个用户脚本都可以定义 `pre_*` 和 `post_*` 脚本，包括复合脚本。
- 每次 `run` 执行都将触发[`pre_run`](https://pdm.fming.dev/latest/plugin/reference/#pdm.signals.pre_run)和[`post_run`](https://pdm.fming.dev/latest/plugin/reference/#pdm.signals.post_run)钩子
- 每次脚本执行都将触发[`pre_script`](https://pdm.fming.dev/latest/plugin/reference/#pdm.signals.pre_script)和[`post_script`](https://pdm.fming.dev/latest/plugin/reference/#pdm.signals.post_script)钩子

给定以下 `scripts` 定义：

```
[tool.pdm.scripts]
pre_script = ""
post_script = ""
pre_test = ""
post_test = ""
test = ""
pre_composite = ""
post_composite = ""
composite = {composite: ["test"]}
```

`pdm run test` 将具有以下生命周期：

```{mermaid}
flowchart LR
  subgraph pdm-run-test [pdm run test]
    direction LR
    pre-run{{Emit pre_run}}
    post-run{{Emit post_run}}
    subgraph run-test [test task]
      direction TB
      pre-script{{Emit pre_script}}
      post-script{{Emit post_script}}
      pre-test[Execute pre_test]
      post-test[Execute post_test]
      test[Execute test]

      pre-script --> pre-test --> test --> post-test --> post-script
    end

    pre-run --> run-test --> post-run
  end
```

当运行 `pdm run composite` 时，将有以下内容：

```{mermaid}
flowchart LR
  subgraph pdm-run-composite [pdm run composite]
    direction LR
    pre-run{{Emit pre_run}}
    post-run{{Emit post_run}}

    subgraph run-composite [composite task]
      direction TB
      pre-script-composite{{Emit pre_script}}
      post-script-composite{{Emit post_script}}
      pre-composite[Execute pre_composite]
      post-composite[Execute post_composite]

      subgraph run-test [test task]
        direction TB
        pre-script-test{{Emit pre_script}}
        post-script-test{{Emit post_script}}
        pre-test[Execute pre_test]
        post-test[Execute post_test]

        pre-script-test --> pre-test --> test --> post-test --> post-script-test
      end

      pre-script-composite --> pre-composite --> run-test --> post-composite --> post-script-composite
    end

     pre-run --> run-composite --> post-run
  end
```
(pdm-hooks:skipping)=
## 跳过执行

使用 `--skip` 选项可以为任何内置命令和自定义用户脚本控制哪个任务和钩子运行。

它接受以逗号分隔的钩子/任务名称列表，以及预定义的 `:all`、`:pre` 和 `:post` 快捷方式，分别跳过所有钩子、所有 `pre_*` 钩子和所有 `post_*` 钩子。您还可以在 `PDM_SKIP_HOOKS` 环境变量中提供跳过列表，但一旦提供了 `--skip` 参数，它就会被覆盖。

对于前面的脚本块，运行 `pdm run --skip=:pre,post_test composite` 将导致以下缩短的生命周期：

```{mermaid}
flowchart LR
  subgraph pdm-run-composite [pdm run composite]
    direction LR
    post-run{{Emit post_run}}

    subgraph run-composite [composite task]
      direction TB
      post-script-composite{{Emit post_script}}
      post-composite[Execute post_composite]

      subgraph run-test [test task]
        direction TB
        post-script-test{{Emit post_script}}

        test --> post-script-test
      end

      run-test --> post-composite --> post-script-composite
    end

     run-composite --> post-run
  end
```
