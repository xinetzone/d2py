from dataclasses import dataclass
import tensorflow as tf

class Unrolled(tf.keras.layers.Layer):
    def __init__(self, obs_shape, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.obs_shape = obs_shape

    # def build(self, input_shape):
    #     self.w, self.h, self.c = self.obs_shape

    def call(self, x):
        """批次中的每个元素都是一个轨迹段（trajectory segment）。
        #（维度是 n segments x n frames per segment x ...）
        # 拼接轨迹段，使第一个维度仅是帧数
        #（这是必要的，因为卷积层对输入形状的要求）
        """
        # Each element of the batch is one trajectory segment.
        # (Dimensions are n segments x n frames per segment x ...)
        # Concatenate trajectory segments so that the first dimension is just
        # frames
        # (necessary because of conv layer's requirements on input shape)
        return tf.reshape(x, [-1, *self.obs_shape])


class Conv2d(tf.keras.Model):
    def __init__(self, filters, kernel_size, strides, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conv2d = tf.keras.layers.Conv2D(
            filters,
            kernel_size,
            strides=strides,
            padding='same', # 'valid'
            data_format=None,
            dilation_rate=(1, 1),
            groups=1,
            activation=None,
            use_bias=True,
            name=name,
        )
        self.leaky_relu = tf.keras.layers.LeakyReLU(negative_slope=0.01)

    def call(self, x):
        x = self.conv2d(x)
        return self.leaky_relu(x)

def net_cnn(obs_shape):
    # Page 15: (Atari)
    # "[The] input is fed through 4 convolutional layers of size 7x7, 5x5, 3x3,
    # and 3x3 with strides 3, 2, 1, 1, each having 16 filters, with leaky ReLU
    # nonlinearities (α = 0.01). This is followed by a fully connected layer of
    # size 64 and then a scalar output. All convolutional layers use batch norm
    # and dropout with α = 0.5 to prevent predictor overfitting"
    return tf.keras.Sequential([
        Unrolled(obs_shape),
        Conv2d(16, 7, 3, "c1",),
        Conv2d(16, 5, 2, "c2",),
        Conv2d(16, 3, 1, "c3",),
        Conv2d(16, 3, 1, "c4", ),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation=None, use_bias=True, name="d1"),
        tf.keras.layers.LeakyReLU(negative_slope=0.01),
        tf.keras.layers.Dense(1, activation=None, use_bias=True, name="d2",),
    ])

@dataclass
class RewardValue:
    r1: tf.Tensor
    r2: tf.Tensor
    rs1: tf.Tensor
    rs2: tf.Tensor
    pred: tf.Tensor

class RewardBlock(tf.keras.Model):
    def __init__(self, core_network, trainable, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rpn = core_network # RewardPredictorNetwork
        self.rpn.trainable = trainable

    def call(self, segment):
        # 预测展开(unrolled)批次中每一帧的奖励
        _r = self.rpn(segment)[:, 0]
        # 形状应该是“展开后的批次大小”
        # 断言“展开后的批次大小”是 'batch size' 乘以 “每段帧数”
        tf.assert_rank(_r, 1)
        # 重新展开为 'batch size' 乘以 “每段帧数”
        # tf.print(tf.shape(segment))
        __r = tf.reshape(_r, tf.shape(segment)[0:2])
        # 断言形状应该是“批次大小”x“每段帧数”
        tf.assert_rank(__r, 2)
        return __r
    
class RewardPredictor(tf.keras.Model):
    """用于预测人类对输入轨迹中每一帧的奖励。该模型通过训练来学习人类在成对轨迹之间的偏好。

    - 网络输入：
        1. `s1`/`s2`: 成对的轨迹。这些是两个不同的轨迹，模型需要比较它们并预测人类的偏好。

    - 网络输出：
        1. `r1`/`r2`: 每个轨迹中每一帧的预测奖励。模型会为每个轨迹中的每个帧生成奖励值，这些值表示人类对该帧的奖励程度。
        2. `rs1`/`rs2`: 每个轨迹在所有帧上的奖励总和。这是通过对每个轨迹中所有帧的奖励进行求和得到的，表示整个轨迹的总奖励。
        3. `pred`: 预测的偏好。模型输出值，表示它预测人类更倾向于选择哪个轨迹（`s1` 或 `s2`）。
    """
    def __init__(self, core_network, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # core_network = net_cnn(obs_shape)
        self.rb1 = RewardBlock(core_network, trainable=True)
        self.rb2 = RewardBlock(core_network, trainable=False)

    def call(self, inputs):
        s1, s2 = inputs
        r1 = self.rb1(s1)
        r2 = self.rb2(s2)
        # 将每个片段中所有帧的奖励求和
        _rs1 = tf.reduce_sum(r1, axis=1)
        tf.assert_rank(_rs1, 1)
        _rs2 = tf.reduce_sum(r2, axis=1)
        tf.assert_rank(_rs2, 1)
        rs1 = _rs1
        rs2 = _rs2
        # 预测每个段的偏好
        _rs = tf.stack([rs1, rs2], axis=1)
        tf.assert_rank(_rs, 2)
        rs = _rs
        _pred = tf.nn.softmax(rs)
        tf.assert_rank(_pred, 2)
        pred = _pred
        return r1, r2, rs1, rs2, pred #RewardValue(r1, r2, rs1, rs2, pred)

# class RewardPredictorLossBlock(tf.keras.Model):
#     """用于预测人类对输入轨迹中每一帧的奖励。该模型通过训练来学习人类在成对轨迹之间的偏好。

#     - 网络输入：
#         1. `s1`/`s2`: 成对的轨迹。这些是两个不同的轨迹，模型需要比较它们并预测人类的偏好。
#         2. `pref`: 每对轨迹之间的偏好。这是人类对这两个轨迹的偏好评分，通常是标量值，表示人类更倾向于选择哪个轨迹。

#     - 网络输出：
#         1. `r1`/`r2`: 每个轨迹中每一帧的预测奖励。模型会为每个轨迹中的每个帧生成奖励值，这些值表示人类对该帧的奖励程度。
#         2. `rs1`/`rs2`: 每个轨迹在所有帧上的奖励总和。这是通过对每个轨迹中所有帧的奖励进行求和得到的，表示整个轨迹的总奖励。
#         3. `pred`: 预测的偏好。模型输出值，表示它预测人类更倾向于选择哪个轨迹（`s1` 或 `s2`）。
#     """
#     def __init__(self, rpb, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # self.RewardPredictorBlock()
#         self.rpb = rpb

#     def call(self, s1, s2, pref):
#         r1, r2, rs1, rs2, pred = self.rpb(s1, s2)
#         preds_correct = tf.equal(tf.argmax(pref, 1), tf.argmax(pred, 1))
#         accuracy = tf.reduce_mean(tf.cast(preds_correct, tf.float32))
#         _loss = tf.nn.softmax_cross_entropy_with_logits_v2(labels=pref,
#                                                            logits=tf.stack([rs1, rs2], axis=1))
#         tf.assert_rank(_loss, 1)
#         loss = tf.reduce_sum(_loss)
#         return accuracy, loss
