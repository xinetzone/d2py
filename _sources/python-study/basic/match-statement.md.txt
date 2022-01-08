# `match` 语句（raw）

Python 3.10 及其以上版本的特性。

`match` 语句接受一个表达式并将它的值与以一个或多个 `case` 语句块形式给出的一系列模式进行比较。这在表面上很类似 C, Java 或 JavaScript（以及许多其他语言）中的 `switch` 语句，但它还能够从值中提取子部分（序列元素或对象属性）并赋值给变量。

最简单的形式是将一个目标值与一个或多个字面值进行比较：

```python
def http_error(status):
    match status:
        case 400:
            return "Bad request"
        case 404:
            return "Not found"
        case 418:
            return "I'm a teapot"
        case _:
            return "Something's wrong with the internet"
```

请注意最后一个代码块: "变量名" `_` 被作为 通配符 并必定会匹配成功。 如果没有任何 `case` 语句匹配成功，则任何分支都不会被执行。

你可以使用 ``|`` （“或”）在一个模式中组合几个字面值：

```python
case 401 | 403 | 404:
    return "Not allowed"
```

模式的形式可以类似于解包赋值，并可被用于绑定变量：

```python
match point:
    case (0, 0):
        print("Origin")
    case (0, y):
        print(f"Y={y}")
    case (x, 0):
        print(f"X={x}")
    case (x, y):
        print(f"X={x}, Y={y}")
    case _:
        raise ValueError("Not a point")
```

请仔细研究此代码！ 第一个模式有两个字面值，可以看作是上面所示字面值模式的扩展。 但接下来的两个模式结合了一个字面值和一个变量，而变量 绑定 了一个来自目标的值（`point`）。 第四个模式捕获了两个值，这使得它在概念上类似于解包赋值 `(x, y) = point`。

如果你使用类来结构化你的数据，你可以使用类名之后跟一个类似于构造器的参数列表，这样能够捕获属性放入到变量中：

```python
class Point:
    x: int
    y: int

def where_is(point):
    match point:
        case Point(x=0, y=0):
            print("Origin")
        case Point(x=0, y=y):
            print(f"Y={y}")
        case Point(x=x, y=0):
            print(f"X={x}")
        case Point():
            print("Somewhere else")
        case _:
            print("Not a point")
```

你可以在某些为其属性提供了排序的内置类（例如 `dataclass`）中使用位置参数。你也可以通过在你的类中设置 `__match_args__` 特殊属性来为模式中的属性定义一个专门的位置。如果它被设为 `("x", "y")`，则以下模式均为等价的（并且都是将 `y` 属性绑定到 `var` 变量）：

```python
Point(1, var)
Point(1, y=var)
Point(x=1, y=var)
Point(y=var, x=1)
```

读取模式的推荐方式是将它们看做是你会在赋值操作左侧放置的内容的扩展形式，以便理解各个变量将会被设置的值。 只有单独的名称（例如上面的 `var`）会被 `match` 语句所赋值。带点号的名称（例如 `foo.bar`）、属性名称（例如上面的 `x=` 和 `y=`） 或类名称（通过其后的 "`(...)`" 来识别，例如上面的 `Point`）都绝不会被赋值。

模式可以任意地嵌套。例如，如果我们有一个由点组成的短列表，则可以这样匹配它：

```python
match points:
    case []:
        print("No points")
    case [Point(0, 0)]:
        print("The origin")
    case [Point(x, y)]:
        print(f"Single point {x}, {y}")
    case [Point(0, y1), Point(0, y2)]:
        print(f"Two on the Y axis at {y1}, {y2}")
    case _:
        print("Something else")
```

我们可以向一个模式添加 `if` 子句，称为“守护项”。 如果守护项为假值，则 `match` 将继续尝试下一个 `case` 语句块。请注意值的捕获发生在守护项被求值之前：

```python
match point:
    case Point(x, y) if x == y:
        print(f"Y=X at {x}")
    case Point(x, y):
        print(f"Not on the diagonal")
```

此语句的一些其他关键特性：

- 类似于解包赋值，元组和列表模式具有完全相同的含义并且实际上能匹配任意序列。一个重要的例外是它们不能匹配迭代器或字符串。
- 序列模式支持扩展解包操作: `[x, y, *rest]` 和 `(x, y, *rest)` 的作用类似于解包赋值。在 `*` 之后的名称也可以为 `_`，因此 `(x, y, *_)` 可以匹配包含至少两个条目的序列而不必绑定其余的条目。
- Mapping patterns: `{"bandwidth": b, "latency": l}` captures the `"bandwidth"` and `"latency"` values from a dictionary. Unlike sequence patterns, extra keys are ignored. An unpacking like `**rest` is also supported. (But `**_` would be redundant, so it is not allowed.)
- 子模式可使用 `as` 关键字来捕获：

    ```python
    case (Point(x1, y1), Point(x2, y2) as p2): ...
    ```

    将把输入的第二个元素捕获为 `p2` （只要输入是包含两个点的序列）

- 大多数字面值是按相等性比较的，但是单例对象 `True`, `False` 和 `None` 则是按标识号比较的。
- 模式可以使用命名常量。这些命名常量必须为带点号的名称以防止它们被解读为捕获变量：

    ```python
    from enum import Enum
    class Color(Enum):
        RED = 'red'
        GREEN = 'green'
        BLUE = 'blue'

    color = Color(input("Enter your choice of 'red', 'blue' or 'green': "))

    match color:
        case Color.RED:
            print("I see red!")
        case Color.GREEN:
            print("Grass is green")
        case Color.BLUE:
            print("I'm feeling the blues :(")
    ```

要获取更详细的说明和额外的示例，你可以参阅以教程格式撰写的 {pep}`636`。

-----

循环 `else` 子句提供了常见的编写代码的明确语法：这是编写代码的结构，让你捕捉循环的“另一条”出路，而不通过设定和检查标志位或条件。

例如，假设你要写一个循环搜索列表的值，而且需要知道在离开循环后该值是否已经找到，可能会用下面的方式编写该任务：

```python
found = False
while x and not found:
    if match(x[0]):
        print('Ni')
        found = True
    else:
        x = x[1:]
if not found:
    print('not found')
```

我们亦可使用循环 `else` 分句来简化上述代码：

```python
while x:
    if match(x[0]):
        print('Ni')
        break
    x = x[1:]
else:
    print('not found')
```