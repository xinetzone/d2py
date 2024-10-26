# Matplotlib 事件处理

Matplotlib 支持使用中立的 GUI 事件模型进行事件处理，因此你可以连接到 Matplotlib 事件而无需了解 Matplotlib 最终将插入到哪个用户界面。这有两个优点：你编写的代码将更具可移植性，而且 Matplotlib 事件知道诸如数据坐标空间以及事件发生在哪个轴上等信息，所以你不必处理从画布空间到数据空间的低级转换细节。还包括对象拾取示例。

```{toctree}
:glob:

*
```
