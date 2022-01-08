# 注解

详见 {pep}`3107` 和 {pep}`484`

## 类型提示

{term}`annotation` 为变量、类属性、函数的形参或返回值指定预期的类型。

类型提示（type hint）属于可选项，Python 不要求提供，但其可对静态类型分析工具起作用，并可协助 IDE 实现代码补全与重构。

全局变量、类属性和函数的类型提示可以使用 {func}`typing.get_type_hints` 来访问，但局部变量则不可以。

## 变量标注

对变量或类属性的 {term}`annotation`。

在标注变量或类属性时，还可选择为其赋值：

```python
class C:
    field: 'annotation'
```

变量标注通常被用作 **类型提示**。例如以下变量预期接受 `int` 类型的值：

```python
count: int = 0
```

##  函数标注

{term}`annotation` 以字典的形式存放在函数的 `__annotations__` 属性中，并且不会影响函数的任何其他部分。形参标注的定义方式是在形参名后加冒号，后面跟一个表达式，该表达式会被求值为标注的值。返回值标注的定义方式是加组合符号 `->`，后面跟一个表达式，该标注位于形参列表和表示 `def` 语句结束的冒号之间。下面的示例有一个必须的参数，一个可选的关键字参数以及返回值都带有相应的标注：

```python
def f(ham: str, eggs: str = 'eggs') -> str:
    print("注解：", f.__annotations__)
    print("参数：", ham, eggs)
    return ham + ' 和 ' + eggs

f('spam')
```

## 在 Python 3.10 以上版本中访问对象的注解字典

Python 3.10 在标准库中加入了一个新函数：{func}`inspect.get_annotations`。在 Python 3.10 以上的版本中，调用该函数就是访问对象注解字典的最佳做法。该函数还可以“解析”字符串形式的注解。

有时会因为某些原因看不到 {func}`inspect.get_annotations`，也可以直接访问 `__annotations__` 数据成员。这方面的最佳实践在 Python 3.10 中也发生了变化：从 Python 3.10 开始，Python 函数、类和模块的 `o.__annotations__` 保证 可用。如果确定是要查看这三种对象，只要利用 `o.__annotations__` 读取对象的注释字典即可。

不过其他类型的可调用对象可能就没有定义 `__annotations__` 属性，比如由 {func}`functools.partial` 创建的可调用对象。当访问某个未知对象的 `__annotations__` 时，Python 3.10 以上版本的最佳做法是带三个参数去调用 {func}`getattr()`，比如 `getattr(o, '__annotations__', None)`。

## 任何版本 Python 中使用 `__annotations__` 的最佳实践

- 应避免直接给对象的 `__annotations__` 成员赋值。请让 Python 来管理 `__annotations__`。
- 如果直接给某对象的 `__annotations__` 成员赋值，应该确保设成一个 {class}`dict` 对象。
- 如果直接访问某个对象的 `__annotations__` 成员，在解析其值之前，应先确认其为字典类型。
- 应避免修改 `__annotations__` 字典。
- 应避免删除对象的 `__annotations__` 属性。
