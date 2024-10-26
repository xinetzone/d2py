# 如何自定义文档内容

使用默认设置，AutoAPI 将记录在 Python 中加载时通过实际包公开访问的所有内容。例如，如果将函数从子模块导入到包中，那么该函数将在子模块和包中同时记录。

然而，有多个选项可用于控制 AutoAPI 将记录的内容。

## 连接到 `autoapi-skip-member` 事件

每当模板必须决定是否应该在文档中包含某个成员时，就会触发 [`autoapi-skip-member`](https://sphinx-autoapi.readthedocs.io/en/latest/reference/config.html#event-autoapi-skip-member) 事件。

例如，要只记录包——换句话说，不记录子模块——您可以在 `conf.py` 中实现事件处理程序，如下所示：

```python
def skip_submodules(app, what, name, obj, skip, options):
    if what == "module":
        skip = True
    elif what == "class" and "util" in name:
       skip = True
    return skip

def setup(app):
    app.connect("autoapi-skip-member", skip_submodules)
```

当模板必须决定是否应将成员包含在文档中时触发。通常，如果处理程序返回 `True`，则跳过该成员，否则包含该成员。处理程序应该返回 `None` 以退回到 AutoAPI 或其他附加处理程序的默认跳过行为。

- `app`：Sphinx 应用对象。
- `what` (str)：文档字符串所属对象的类型。可以是： `"attribute"`、`"class"`、`"data"`、`"exception"`、`"function"`、`"method"`、`"module"`、`"package"`。
- `name` (str)：对象的完全限定名。
- `obj` (PythonPythonMapper)：对象本身。
- `skip` (bool)：如果处理程序不覆盖该决定，AutoAPI 是否会跳过该成员。
- `options`：给指令的选项。

## 设置 `__all__`

AutoAPI 将 `__all__` 的定义视为模块或包中哪些对象是公共的，哪些不是公共的。

在下面的示例中，只记录了 `func_a()` 和 `A`。

```python
# mypackage/__init__.py
from . import B

__all__ = ("A", "func_a")

class A:
    ...

def func_a():
    ...

def func_b():
    ...
```

## 配置 `autoapi_options`

`autoapi_options` 配置值对记录的内容提供了一些高级控制。例如，您可以隐藏没有文档字符串的成员、文档私有成员和隐藏魔术方法。有关如何使用此选项的更多信息，请参阅 [`autoapi_options`](https://sphinx-autoapi.readthedocs.io/en/latest/reference/config.html#confval-autoapi_options)。

## 自定义 API 文档模板

最后，您可以通过定制模板来配置呈现的内容。这是一种相当严厉的方法，所以只有当其他选项不能给您所需的控制时才需要使用它。你可以在下一节学习如何定制模板；如何[通过模板自定义布局](customise-templates)。
