# `abc` 抽象基类

鸭子类型
:   一种编程风格（duck-typing），它并不依靠查找对象类型来确定其是否具有正确的接口，而是直接调用或使用其方法或属性（“看起来像鸭子，叫起来也像鸭子，那么肯定就是鸭子。”）由于强调接口而非特定类型，设计良好的代码可通过允许多态替代来提升灵活性。鸭子类型避免使用 {class}`type`() 或 {func}`isinstance` 检测。（但要注意鸭子类型可以使用 抽象基类 作为补充。） 而往往会采用 {func}`hasattr` 检测或是 {term}`EAFP` 编程。

抽象基类
:   抽象基类简称 ABC（abstract base class）是对 {dfn}`鸭子类型` 的补充。它提供了一种定义接口的新方式，相比之下其他技巧例如 {func}`hasattr` 显得过于笨拙或有微妙错误（例如使用 **魔术方法**）。ABC 引入了虚拟子类，这种类并非继承自其他类，但却仍能被 {func}`isinstance` 和 {func}`issubclass` 所认可；详见 {mod}`abc` 模块文档。Python 自带许多内置的 ABC 用于实现数据结构（在 {mod}`collections.abc` 模块中）、数字（在 {mod}`numbers` 模块中）、流（在 {mod}`io` 模块中）、导入查找器和加载器（在 {mod}`importlib.abc` 模块中）。你可以使用 {mod}`abc` 模块来创建自己的 ABC。