# Replite 指令

`jupyterlite-sphinx` 提供了 `replite` 指令，允许你在文档中嵌入 replite 控制台。这个指令接受额外的选项，这些选项与 `replite` 包的选项相同，可以参考 <https://github.com/jtpio/replite> 获取参考信息。

```rst
.. replite::
   :kernel: xeus-python
   :height: 600px
   :prompt: Try Replite!
   :prompt_color: #dc3545

   import matplotlib.pyplot as plt
   import numpy as np

   x = np.linspace(0, 2 * np.pi, 200)
   y = np.sin(x)

   fig, ax = plt.subplots()
   ax.plot(x, y)
   plt.show()
```

```{eval-rst}
.. replite::
   :kernel: xeus-python
   :height: 600px
   :prompt: Try Replite!
   :prompt_color: #dc3545

   import matplotlib.pyplot as plt
   import numpy as np

   x = np.linspace(0, 2 * np.pi, 200)
   y = np.sin(x)

   fig, ax = plt.subplots()
   ax.plot(x, y)
   plt.show()
```
