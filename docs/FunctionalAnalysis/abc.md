# 抽象基类

模块 {mod}`~abc.ABC` 全称 Abstract Base Classes，简写为 ABC。ABC 可以像 mix-in 类一样直接被子类继承。你也可以将不相关的具体类（包括内建类）和抽象基类注册为“抽象子类” —— 这些类以及它们的子类会被内建函数 {func}`issubclass` 识别为对应的抽象基类的子类，但是该抽象基类不会出现在其 MRO（Method Resolution Order，方法解析顺序）中，抽象基类中实现的方法也不可调用（即使通过 {class}`super` 调用也不行）

```python
from abc import ABC, abstractmethod
```