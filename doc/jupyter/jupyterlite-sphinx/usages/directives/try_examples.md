# TryExamples 指令

`jupyterlite-sphinx` 提供了实验性的 `try_examples` 指令，它允许使用[doctest格式](https://docs.python.org/3/library/doctest.html)编写的 docstring 示例部分与嵌入式经典 Notebook 进行交换。

这是使用指令的示例。按钮已经通过自定义 CSS 进行了样式设置，具体设置方法请参考下面的配置部分。如果没有自定义 CSS，按钮将保持简单且无装饰。


```rst
Examples
--------
.. try_examples::

    Doctest examples sections are parsed and converted to notebooks. Blocks of text
    like this become markdown cells. Codeblocks begin with ``>>>``. Contiguous blocks
    of code are combined into a single code cell.

    >>> x = 2
    >>> y = 2
    >>> x + y
    4

    ``...`` is used to continue multiline statements.

    >>> def f(x, y):
    ...     return x + y
    >>> f(2, 2)
    4

    Inline LaTeX like :math:`x + y = 4` is converted, as is block LaTeX like

    .. math::

        \int_{x=-\infty}^{\infty}e^{-x^2}\mathrm{d}x = \sqrt{\pi}

    If you are displaying `math output <https://www.sphinx-doc.org/en/master/usage/extensions/math.html>`_
    with sphinx. Sphinx links such as the one in the previous sentence are also converted to
    markdown format.
```

这里是渲染后的外观和工作方式。


```{eval-rst}
Examples
--------
.. try_examples::

    Doctest examples sections are parsed and converted to notebooks. Blocks of text
    like this become markdown cells. Codeblocks begin with `>>>`. Contiguous blocks
    of code are combined into a single code cell.

    >>> x = 2
    >>> y = 2
    >>> x + y
    4

    `...` is used to continue multiline statements.

    >>> def f(x, y):
    ...     return x + y
    >>> f(2, 2)
    4

    Inline LaTeX like :math:`x + y = 4` is converted, as is block LaTeX like

    .. math::

        \int_{-\infty}^{\infty}e^{-x^2}\mathrm{d}x = \sqrt{\pi}

    If you are displaying `math output <https://www.sphinx-doc.org/en/master/usage/extensions/math.html>`_
    with sphinx. Sphinx links such as the one in the previous sentence are also converted to
    markdown format.
```

默认情况下，嵌入式笔记本的 `iframe` 容器的高度会计算以匹配渲染后的 doctest 示例的高度，以便在页面上占用相同的空间。

## 配置

按钮的位置和样式可以通过添加自定义CSS来定制，以匹配你的文档设计，具体方法请参考Sphinx的文档[这里](https://docs.readthedocs.io/en/stable/guides/adding-custom-css.html#how-to-add-custom-css-or-javascript-to-sphinx-documentation)。按钮的类名为 `try_examples_button`。按钮放置在类名为 `try_examples_button_container` 的容器内，可以选择这些容器来调整按钮的位置。上述示例的 CSS 为

```css

.try_examples_button {
    color: white;
    background-color: #0054a6;
    border: none;
    padding: 5px 10px;
    border-radius: 10px;
    margin-bottom: 5px;
    box-shadow: 0 2px 5px rgba(108,108,108,0.2);
}

.try_examples_button:hover {
    background-color: #0066cc;
    transform: scale(1.02);
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    cursor: pointer;
}

.try_examples_button_container {
    display: flex;
    justify-content: flex-end;
}
```

`try_examples` 指令有选项
* `:height:` 用于设置包含嵌入式笔记本的[iframe](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe)的高度的具体值。
* `:button_text:` 用于自定义按钮的文本，该按钮将渲染后的示例替换为嵌入式笔记本。
* `:theme:` 与其他 JupyterLite-Sphinx 指令的工作方式相同。
* `:example_class:` html 类，附加到渲染示例内容和嵌入式笔记本的外部容器。这可以在自定义 css 文件中使用，以允许更精确的定制，例如在不同的示例中应用不同的按钮样式。

这里是设置了某些选项的示例

```rst
.. try_examples::
    :button_text: Try it in your browser!
    :height: 400px

    The button text has changed and the height now exceeds the size of the content.

    >>> x = 2
    >>> y = 2
    >>> x + y
    4

    We've also added the ``blue-bottom`` class, the button should appear as blue,
    below the examples, and on the left side of the screen.

    See `try_examples.css <https://github.com/jupyterlite/jupyterlite-sphinx/blob/main/docs/_static/try_examples.css>`_
    to see how we achieved this via custom css.
```

结果：

```{eval-rst}
.. try_examples::
    :button_text: Try it in your browser!

    The button text has changed and the height now exceeds the size of the content.

    >>> x = 2
    >>> y = 2
    >>> x + y
    4

    We've also added the ``blue-bottom`` class, the button should appear as blue,
    below the examples, and on the left side of the screen.

    See `try_examples.css <https://github.com/jupyterlite/jupyterlite-sphinx/blob/main/docs/_static/try_examples.css>`_
    to see how we achieved this via custom css.
```

### 全局配置

对于包含大量现有doctest示例的项目，手动为每个docstring示例添加`try_examples`指令可能会非常繁琐。如果你正在使用[sphinx.ext.autodoc](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html)与[numpydoc](https://numpydoc.readthedocs.io/en/latest/format.html)或[sphinx.ext.napoleon](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html)，你可以在你的sphinx `conf.py`中设置以下选项：

```python
global_enable_try_examples = True
```

这将在 `"autodoc-process-docstring"` 事件期间自动在示例部分插入 `try_examples` 指令。这是通过识别部分标题来实现的。示例部分包括示例标题下的所有内容，直到下一个标题或docstring的结尾（如果没有更多的标题）。需要使用 `numpydoc` 或 `sphinx.ext.napoleon` 之一，因为它们将这些部分标题映射到标准化格式。

如果示例部分已经包含 `try_examples` 指令，将不会插入额外的指令，允许在需要时单独配置特定情况。在示例部分的部分标题下的第一行非空行添加注释：

```rst
..! disable_try_examples`
```

将阻止插入指令，允许指定不应变为交互式的示例部分。

按钮文本和主题可以通过配置变量 `try_examples_global_button_text` 和 `try_examples_global_theme` 全局设置。

```python
global_enable_try_examples = True
try_examples_global_button_text = "Try it in your browser!"
try_examples_global_height = "200px"
```

由于适当的高度应取决于示例内容的大小，因此没有设置全局特定高度的选项。再次强调，嵌入式笔记本的iframe容器的默认高度与关联的渲染doctest示例的高度相匹配，以便在页面上占用相同的空间。对于非常小的示例，这可能会导致一个无法使用的小型笔记本。可以在下面描述的 `try_examples.json` 配置文件中设置全局最小高度。

### try_examples.json 配置文件

用户可以在他们的文档源根目录中放置一个名为 `try_examples.json` 的配置文件。这个配置文件将被复制到部署文档的构建根目录中。在构建根目录中对配置文件的更改将会被尊重，无需重新构建文档，允许运行时配置。

当前的选项有：

#### "ignore_patterns"

格式是一个列表，其中包含附加到键 `"ignore_patterns"` 的[JavaScript正则表达式模式](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_expressions)，如下所示。

```json
{
    "ignore_patterns": ["^/latest/.*", "^/stable/reference/generated/example.html"]
}
```

在与这些模式中至少一个匹配的 URL 路径名中，`TryExamples` 按钮将被隐藏，从而有效地禁用交互式文档。在提供的例子中：

* 模式 `"^/latest/.*"` 禁用了针对最新版本包的文档 URL 的交互式示例，如果这份文档是针对开发版本的，并且相应的包构建在 Jupyterlite 内核中不可用，这可能会很有用。

* 模式 `"^/stable/reference/generated/example.html"` 针对最新稳定版本文档中的特定 URL。

注意，这些模式应该匹配 URL 的[路径名](https://developer.mozilla.org/en-US/docs/Web/API/Location/pathname)，而不是完整的URL。这是 URL 的路径部分。例如，https://jupyterlite-sphinx.readthedocs.io/en/latest/directives/try_examples.html 的路径名是 `/en/latest/directives/try_examples.html`。

再次强调，配置文件可以在部署的文档中添加或编辑，允许在不重新构建文档的情况下禁用或启用示例。

#### "global_min_height"

为了避免由于默认设置（嵌入式笔记本的iframe容器占用与替换的渲染内容相同的空间）而导致非常小的示例具有无法使用的小型笔记本，用户可以在 `try_examples.json` 中设置全局最小高度。

```json
{
    "global_min_height": "400px"
}
```

这允许在不重新构建文档的情况下设置或更改最小高度。当为 `.. try_examples::` 提供特定高度的选项时，此配置值将被忽略。

## 其他注意事项

如果您在文档中使用 `TryExamples` 指令，您需要确保在您使用的 Jupyterlite 内核中安装的包版本与您要记录的版本相匹配。
