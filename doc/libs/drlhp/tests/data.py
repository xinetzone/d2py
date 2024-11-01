import tensorflow as tf
import tensorflow.experimental.numpy as tnp
from drlhp.model import RewardPredictor, net_cnn

@tf.function
def fake_data(n_segs, n_frames):
    s1s = tf.TensorArray(dtype=tf.float64, size=0, dynamic_size=True)
    s2s = tf.TensorArray(dtype=tf.float64, size=0, dynamic_size=True)
    for i in tf.range(n_segs):
        s1 = 255 * tnp.random.rand(n_frames, 84, 84, 4)
        s2 = 255 * tnp.random.rand(n_frames, 84, 84, 4)
        s1s = s1s.write(i, s1)
        s2s = s2s.write(i, s2)
    s1s = s1s.stack()
    s2s = s2s.stack()
    return s1s, s2s

# n_segs = 2
# obs_shape = (84, 84, 4)
# n_frames = 20
# prefs = [[0., 1.], [1., 0.]]
# s1s, s2s = fake_data(n_segs, n_frames)
# core_network = net_cnn(obs_shape)
# rpn = RewardPredictor(core_network)
# rpn.compile(optimizer='adam',
#             loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
#             metrics=['accuracy'])
# r1_batch, r2_batch, rs1_batch, rs2_batch, pred_batch = rpn([s1s, s2s])
# rs_batch = tf.stack([rs1_batch, rs2_batch], axis=1)