# 对抗样本

{cite:p}`szegedy2014intriguing` 发现对数据添加一些微小的扰动就可以改变模型的分类结果，甚至还可以通过添加扰动让模型对不同的数据产生相同的分类结果。他们将这种人眼看来没有区别，但是模型却分错了样本称为对抗样本。

寻找对抗样本的过程被他们定义为优化问题：

对数据 $\mathbf{x}$ 和错误标签 $\mathbf{l}$，寻找最小的扰动 $\mathbf{r^*}$ 使得分类器 $f: \R^m \to \{1, \cdots, k\}$ 将 $\mathbf{x+r^*}$ 错误分类为 $\mathbf{l}$，即

$$
\mathbf{r}^* = \arg\min_{\mathbf{r}}||r||_2\\
\text{s.t.} f(\mathbf{x+r}) = \mathbf{l}, \mathbf{x+r}\in [0,1]^m
$$

生成的扰动 $r^*$ 即对抗扰动，扰动后的数据 $x+r^*$ 即是对抗样本。

不过，他们实际求解的是下面这个优化问题：

$$
\mathbf{r}^* = \arg\min_{\mathbf{r}} c|r| + L(\theta, \mathbf{x+r}, \mathbf{l})
\\
\text{s.t.} f(\mathbf{x+r}) = \mathbf{l}, \mathbf{x+r}\in [0,1]^m
$$

其中 $L$ 是损失函数， $\theta$ 是模型的参数。

这个形式非常有意思，因为如果把优化的对象换成 $\theta$，再把错误标签 \mathbf{l} 换成数据对应的正确标签 \mathbf{y}，那这就是训练模型的标准优化过程。**何为对抗？不再优化参数，而是优化输入——更加确切地说，优化输入数据的噪声。**