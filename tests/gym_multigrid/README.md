# Gymnasium 示例
一些简单的Gymnasium环境和包装器的示例。
有关这些示例的一些解释，请参阅[Gymnasium文档](https://gymnasium.farama.org)。

### 环境
这个存储库托管了在[环境创建文档](https://gymnasium.farama.org/tutorials/gymnasium_basics/environment_creation/)中显示的示例。
- `GridWorldEnv`: 网格世界环境的简单实现

### 包装器
这个存储库托管了在[包装器文档](https://gymnasium.farama.org/api/wrappers/)中显示的示例。
- `ClipReward`: `RewardWrapper`，将即时奖励裁剪到有效范围
- `DiscreteActions`: `ActionWrapper`，将动作空间限制为有限的子集
- `RelativePosition`: `ObservationWrapper`，计算代理和目标之间的相对位置
- `ReacherRewardWrapper`: 允许我们对 reacher 环境的奖励项进行加权

## 安装

要安装您的新环境，请运行以下命令：

```shell
cd gym_multigrid
pip install -e .
```