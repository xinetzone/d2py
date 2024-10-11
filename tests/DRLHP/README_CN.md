# 从人类偏好中学习的深度强化学习

这段代码是基于 OpenAI 和 DeepMind 的 [《从人类偏好中学习的深度强化学习》](https://blog.openai.com/deep-reinforcement-learning-from-human-preferences/)复现，由 Matthew Rahtz 完成，并经过重构以便于在加州大学伯克利分校人类兼容人工智能研究中心的研究应用中使用。Matthew Rahtz 编写的原始代码可以在[这里](https://github.com/mrahtz/learning-from-human-preferences)找到。重构工作主要由 Cody Wild 在 2020 年春季完成。

## 重构

### 目标

原始版本的代码库的目标是成功训练 DRLHP（Deep Reinforcement Learning from Human Preferences），使用合成和人类的偏好在 Pong、Enduro 和新颖的移动点环境中进行训练，其 API 主要设计用于这些小型重现案例。重构的目标包括：

* 将 API 从单一 `run.py` 文件更改为更模块化的设计，以便可以插入其他实验代码
* 添加对任意像素基础环境的支持，具有不同大小和通道数
* 允许更容易地与更广泛的最新 RL 实现集成，而不是在代码库中有特定的 A2C 实现
* 简化加载预训练策略（无论是来自 RL 还是模仿）以预热训练过程的过程，除了从头开始启动策略外

### 设计

为了实现这些目标，DRLHP 的基本元素被重构为 Gym 风格的环境包装器。这个包装器：

* 管理创建子进程，用于异步奖励预测器训练和异步收集偏好对的片段
* 存储从底层环境返回的观察结果，将它们连接成片段。当片段达到指定长度时，它们会通过管道传递给负责构建片段对并请求偏好的子进程
* 可以返回底层环境的奖励或奖励预测器的奖励，该奖励预测器在整个奖励预测器训练过程中加载和更新
* 可以与任何兼容 Gym 的 RL 算法一起使用，可以将奖励预测器奖励传递给它，而无需对其进行特殊修改

## 设置

此仓库被组织成 Python 包，可以通过运行以下命令安装：

```python
python setup.py install
```

如果您希望开发该软件包，可以使用 `-e` 选项以可编辑模式安装一些可选的软件包：

```python
pip install -e .[dev]
```

测试可以通过运行以下命令进行：

```python
pytest tests/
```

## 人类偏好 GUI

当使用人类而非合成偏好进行训练时，您会看到两个窗口：一个显示代理行为示例的大窗口，另一个显示代理最后完整情节的小窗口（这样您可以查看定性行为是如何变化的）。在终端中输入 'L' 表示您更喜欢左侧示例；输入 'R' 表示您更喜欢右侧示例；输入 'E' 表示您认为它们都相等；如果两个片段无法比较，请按回车键。

好的，下面是你提供的文本的翻译：

## 工作流程

一旦安装了 `drlhp` 包，你可以通过以下方式导入环境包装器（算法的主要入口点）：
`from drlhp import HumanPreferencesEnvWrapper`

要构建 DRLHP 环境，请使用所选的基础环境作为参数调用包装器。此 DRLHP 实现设计用于处理像素观测值，因此您选择要包装的环境应满足以下条件之一：（1）返回像素作为观测值，或（2）返回可以转换为像素的观测值（例如，可以索引到的dict空间）。如果您的环境属于后一种情况，您可以使用 `obs_transform_func` 指定一个函数来映射您的观测值与像素之间。

EnvWrapper 接受多个不同的参数，并设计为支持多种不同的工作流程。下面是这些工作流程的一系列（非详尽！）示例。

### 默认 - 收集人类偏好并训练奖励模型

```python
wrapped_env = HumanPreferencesEnvWrapper(env, 
                                         segment_length=100,
                                         synthetic_preferences=False, 
                                         n_initial_training_steps=10)
```

上述代码将创建一个环境，该环境将启动偏好获取和奖励训练进程，并在奖励模型经过10个训练步骤后切换为返回预测奖励作为环境奖励。合成偏好默认设置为 `True`，但在这里我们将其设置为 `False`，以表示希望运行PrefInterface GUI。

### 收集偏好但不训练奖励模型

```python
wrapped_env = HumanPreferencesEnvWrapper(env, 
                                         synthetic_preferences=False,
                                         collect_prefs=True, 
                                         train_reward=False, 
                                         log_dir=<log_dir>)
```

如果你想要批量收集偏好以便稍后在训练中使用，这个工作流程可能会很有用。当你想将偏好保存到文件时，可以调用 `wrapped_env.save_prefs()`。默认情况下，偏好会保存到 `log_dir` 内的 `train.pkl.gz` 和 `val.pkl.gz`。

### 从预先收集的偏好中训练奖励模型

```python
wrapped_env = HumanPreferencesEnvWrapper(env, 
                                         prefs_dir=<prefs_dir>,
                                         collect_prefs=False, 
                                         train_reward=True, 
                                         reward_predictor_ckpt_interval=10)
```

这将从 `prefs_dir` 中加载偏好数据库并使用它来训练奖励模型，该模型将每 10 个训练步骤保存一次检查点到 `<log_dir>/reward_predictor_checkpoints/reward_predictor.ckpt`。默认情况下，`log_dir` 被设置为 `drlhp_logs`。

### 使用预训练的奖励模型而不进行额外训练

```python
wrapped_env = HumanPreferencesEnvWrapper(env, 
                                         pretrained_reward_predictor_dir='my_log_dir/reward_predictor_checkpoints/',
                                         collect_prefs=False, 
                                         train_reward=False)
```

要确认环境是否正在使用训练过的奖励模型而不是基础环境的奖励，请检查 `using_reward_from_predictor` 标志是否设置为 `True`。如果在某个时刻你想切换回基础环境的奖励（例如，用于评估目的），可以调用 `wrapped_env.switch_to_true_reward()` 进行切换，以及 `wrapped_env.switch_to_predicted_reward()`。

## 架构

除了环境包装器本身，还有三个主要组件：

* 偏好界面（`pref_interface.py`）
* PrefBuffer 和 PrefDB（`pref_db.py`）
* 奖励预测器（`reward_predictor.py`）

### 数据流

通过从基础环境中返回的环境观察帧积累构建片段，这些片段达到 `segment_length` 时被连接成片段。当一个片段完成后，它会被发送到 PrefInterface（通过多进程队列）。

PrefInterface 将成对的片段组合在一起，并通过命令行界面请求用户对它们进行偏好排序，要么使用合成偏好，要么将每个片段（一组图像帧）渲染为视频剪辑展示给用户。在向用户展示剪辑后，它会询问用户哪一对剪辑更符合用户想要的行为，循环播放视频直到得到响应。

偏好标签通过 PrefBuffer 发送到 PrefDB（训练或验证），PrefBuffer 负责将每个偏好引导到相应的数据库。然后，PrefDB 中的偏好用于训练神经网络奖励预测器，为优选片段分配高标量奖励。

该网络可以用于通过输入剪辑、运行前向传递计算“用户喜欢这个剪辑的程度”值，然后将结果标准化为零均值和时间上的常数方差，从而为未来的视频剪辑预测奖励。

这个标准化值随后被用作奖励信号，由环境传回。

### 进程

这段代码生成两个不同的子进程，除主进程外：

* 一个用于运行偏好界面以查询用户的偏好。
* 一个用于训练奖励预测器。

这些进程通过一组队列进行通信：

* `seg_pipe`，将片段发送到 PrefInterface。
* `pref_pipe`，将来自 PrefInterface 的（片段，偏好标签）对发送到 PrefDB 以添加到 PrefDB 中。

一些棘手的方面包括：
* 必须通过一个小队列将视频剪辑从环境包装器发送给请求偏好的进程；如果队列已满，剪辑将被丢弃。偏好界面然后在0.5秒内从队列中获取尽可能多的剪辑，在询问每对剪辑之间。要展示给用户的剪辑对是从存储来自队列的剪辑的内部偏好界面剪辑数据库中选择的。
* 必须通过一个队列将偏好从偏好界面发送到 PrefDB，进而提供给奖励预测器。然而，偏好绝不应被丢弃，因此偏好界面会阻塞，直到可以将偏好添加到队列中，并且奖励预测器训练过程运行一个后台线程，不断从队列中接收，将偏好存储在奖励预测器进程的内部数据库中。

## 论文设置的更改

对于最初在复制品中测试的环境，即使没有实现原始论文中描述的一些功能，也可以达到上述结果部分中的里程碑。

* 对于奖励预测器网络的正则化，论文使用了dropout、batchnorm和自适应L2正则化方案。在这里，我们只使用dropout。（也支持batchnorm。未实现L2正则化。）
* 在论文的设置中，请求偏好的速率随时间逐渐减少。我们只是以恒定的速率请求偏好。
* 论文根据奖励预测器的预测不确定性选择展示给用户的视频剪辑。早期实验表明，仅随机选择视频剪辑有更高的成功训练机会（论文在某些情况下也提到了这一点），所以我们不做任何集成。（集成代码确实在 `reward_predictor.py` 中实现，但我们始终只操作单个成员的集成，而 `pref_interface.py` 只是随机选择片段。）
* 根据每个剪辑的预测潜在奖励值进行softmax计算每对视频剪辑的偏好。在论文中，“与其直接应用 softmax…… 我们假设人类有 $10\%$ 的机会均匀地随机反应。从概念上讲，需要这种调整是因为人类评分者有恒定的错误概率，随着奖励差异变得极端，错误概率不会衰减到0。”我不确定如何实现这一点——至少，我看不出一种实际影响梯度的方法——所以我们直接做 softmax。

## 代码致谢

所有文件除了 HumanPreferencesEnvWrapper 主要是由 Matthew Rahtz 编写的，作为这次重构的一部分进行了一些微小的更改。
