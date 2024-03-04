# 在其他环境中嵌入 Jupyter 小部件，而非笔记本

Jupyter 交互式小部件可以被序列化并嵌入到以下环境中：

- 静态网页
- Sphinx 文档
- 在 nbviewer 上转换的 HTML 笔记本

在这里，我们讨论使用 `@jupyter-widgets/html-manager` npm 包中的自定义小部件管理器来嵌入小部件。提供了两种嵌入器：

1. 一个基本嵌入器，仅嵌入标准控件，但可以用于任何网页
2. 一个使用 RequireJS 的嵌入器，可以嵌入标准和自定义小部件

## 在 HTML 网页中嵌入小部件

经典的笔记本界面提供了一个 `Widgets` 菜单，用于生成 HTML 片段，可以嵌入到任何静态网页中：

该菜单提供三组操作：

- 保存笔记本小部件状态和清除笔记本小部件状态
- 下载小部件状态
- 嵌入小部件

### 保存笔记本小部件状态

笔记本文件可以与当前小部件状态作为元数据一起保存。这允许使用呈现的小部件渲染笔记本文件（例如，参见下面关于 Sphinx 的部分）。要保存具有当前小部件状态的笔记本，请使用 `Save Notebook Widget State` 菜单项。

为了删除旧的保存状态并将新状态保存到笔记本，请按顺序执行以下操作：

1. 使用 `Clear Notebook Widget State` 菜单并保存笔记本。这将清除笔记本文件中的元数据。
2. 重启内核并刷新页面。这将清除页面上的小部件管理器中的旧小部件状态。
3. 创建您想要的任何小部件，然后使用 `Save Notebook Widget State` 并保存笔记本。这将新的小部件状态保存到笔记本文件中。

### 可嵌入的 HTML 片段

`嵌入小部件` 菜单项提供了一个对话框，其中包含一个嵌入了当前小部件的 HTML 页面。为了支持自定义小部件，它使用了 RequireJS 嵌入器。

这个 HTML 片段由多个嵌入到 HTML 文档中的 `<script>` 标签组成：

- 第一个脚本标签从 CDN 加载 RequireJS。如果您的页面上已经有 RequireJS，可以删除这个脚本标签。

- 第二个脚本标签加载 RequireJS 小部件嵌入器。这定义了适当的模块，然后设置了一个函数来呈现页面上包含的所有小部件视图。如果您只嵌入标准小部件并且不想使用 RequireJS，可以用加载标准嵌入器的脚本标签替换这两个脚本标签。

- 接下来的脚本标签是具有 mime 类型 `application/vnd.jupyter.widget-state+json` 的脚本标签，其中包含当前使用的所有小部件模型的状态。这个脚本标签的内容的 JSON 模式在 `@jupyter-widgets/schema` npm 包中定义。

- 然后有多个脚本标签，每个都有 mime 类型 `application/vnd.jupyter.widget-view+json`，对应于您希望在网页上显示的视图。这些脚本标签必须在页面的主体中，并且会被呈现的小部件替换。这些脚本标签内容的 JSON 模式在 `@jupyter-widgets/schema` npm 包中定义。

当前的“嵌入小部件”操作会为笔记本中显示的每个视图创建一个这样的脚本标签。如果您想布局视图或仅包含其中的一些，可以按您的意愿删除或包含这些脚本标签。

为了清除前端的小部件状态，使其不在嵌入中显示，请按顺序重启内核并刷新页面。

### 小部件状态 JSON

`下载小部件状态` 选项会触发下载一个 JSON 文件，该文件包含当前使用的所有小部件模型的序列化状态，使用 `@jupyter-widgets/schema` npm 包中指定的 `application/vnd.jupyter.widget-state+json` 格式。

## Python 接口

从 Python 中也可以生成用于嵌入的部件代码。`ipywidgets.embed` 模块提供了几个用于以编程方式将部件嵌入到 HTML 文档中的函数。

使用 `embed_minimal_html` 创建一个简单的独立 HTML 页面：

```python
from ipywidgets import IntSlider
from ipywidgets.embed import embed_minimal_html

slider = IntSlider(value=40)
embed_minimal_html('export.html', views=[slider], title='Widgets export')
```

这将创建一个独立的文件 `export.html`。要查看该文件，可以启动一个 HTTP 服务器，例如 Python 标准库中的 [HTTP server](https://docs.python.org/3.6/library/http.server.html#module-http.server)，或者直接在 web 浏览器中打开它（通过双击文件，或在浏览器搜索栏中输入 `file:///path/to/file`）。

有时你可能需要比 `embed_minimal_html` 提供的更细粒度的控制。通常，你会希望控制部件嵌入其中的 HTML 文档的结构。为此，使用 `embed_data` 获取部件状态的特定部分的 JSON 导出。你可以将这些嵌入到 HTML 模板中：

```python
import json

from ipywidgets import IntSlider
from ipywidgets.embed import embed_data

s1 = IntSlider(max=200, value=100)
s2 = IntSlider(value=40)
data = embed_data(views=[s1, s2])

html_template = """
<html>
  <head>

    <title>Widget export</title>

    <!-- Load RequireJS, used by the IPywidgets for dependency management -->
    <script
      src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.4/require.min.js"
      integrity="sha256-Ae2Vz/4ePdIu6ZyI/5ZGsYnb+m0JlOmKPjt6XZ9JJkA="
      crossorigin="anonymous">
    </script>

    <!-- Load IPywidgets bundle for embedding. -->
    <script
      data-jupyter-widgets-cdn="https://unpkg.com/"
      data-jupyter-widgets-cdn-only
      src="https://cdn.jsdelivr.net/npm/@jupyter-widgets/html-manager@*/dist/embed-amd.js"
      crossorigin="anonymous">
    </script>

    <!-- The state of all the widget models on the page -->
    <script type="application/vnd.jupyter.widget-state+json">
      {manager_state}
    </script>
  </head>

  <body>

    <h1>Widget export</h1>

    <div id="first-slider-widget">
      <!-- This script tag will be replaced by the view's DOM tree -->
      <script type="application/vnd.jupyter.widget-view+json">
        {widget_views[0]}
      </script>
    </div>

    <hrule />

    <div id="second-slider-widget">
      <!-- This script tag will be replaced by the view's DOM tree -->
      <script type="application/vnd.jupyter.widget-view+json">
        {widget_views[1]}
      </script>
    </div>

  </body>
</html>
"""

manager_state = json.dumps(data['manager_state'])
widget_views = [json.dumps(view) for view in data['view_specs']]
rendered_template = html_template.format(manager_state=manager_state, widget_views=widget_views)
with open('export.html', 'w') as fp:
    fp.write(rendered_template)
```

网页需要加载 RequireJS 和 Jupyter 部件 HTML 管理器。然后你需要在文档头部的 `<script>` 标签中包含管理器状态，类型为 `application/vnd.jupyter.widget-state+json`。对于每个部件视图，在应包含视图的 DOM 元素中放置一个类型为 `application/vnd.jupyter.widget-view+json` 的 `<script>` 标签。部件管理器将用与部件对应的 DOM 树替换每个 `<script>` 标签。

在这个例子中，我们使用了一个 Python 字符串作为模板，并使用 `format` 方法插入状态。对于嵌入到更复杂文档中，你可能想要使用像 [Jinja2](http://jinja.pocoo.org/) 这样的模板引擎。

我们还通过设置 `data-jupyter-widgets-cdn` 属性将其 CDN 更改为默认的 jsdelivr 以使用 unpkg。

此外，我们通过设置 `data-jupyter-widgets-cdn-only` 属性仅从 CDN 加载模块。

在 `ipywidgets.embed` 中的所有嵌入函数中，默认情况下都会包括部件管理器所知的所有部件的状态。你也可以选择传递一个简化的状态来代替。如果你有许多独立的部件具有大量状态，但只想在导出中包含相关部件，这可能特别相关。要仅包含特定视图及其依赖项的状态，请使用 `dependency_state` 函数：

```python
from ipywidgets.embed import embed_minimal_html, dependency_state

s1 = IntSlider(max=200, value=100)
s2 = IntSlider(value=40)
embed_minimal_html('export.html', views=[s1, s2], state=dependency_state([s1, s2]))
```

## 在Sphinx HTML文档中嵌入小部件

从ipywidgets 6.0开始，Jupyter交互式小部件可以在Sphinx html文档中呈现。提供了两种实现方法：

### 使用Jupyter Sphinx扩展

[jupyter_sphinx](https://jupyter-sphinx.readthedocs.io)扩展
在sphinx中启用了jupyter特定的功能。可以使用`pip`和`conda`进行安装。

在`conf.py` sphinx配置文件中，将`jupyter_sphinx`添加到启用的扩展列表中。

然后使用`jupyter-execute`指令将代码执行的输出嵌入到文档中：

```rst
.. jupyter-execute::

  from ipywidgets import VBox, jsdlink, IntSlider, Button
  s1, s2 = IntSlider(max=200, value=100), IntSlider(value=40)
  b = Button(icon='legal')
  jsdlink((s1, 'value'), (s2, 'max'))
  VBox([s1, s2, b])
```

### 使用`nbsphinx`项目

[nbsphinx](https://nbsphinx.readthedocs.io/) Sphinx扩展
为`*.ipynb`文件提供了一个源解析器。自定义Sphinx指令用于显示Jupyter Notebook代码单元格（以及它们的

## 在[nbviewer](http://nbviewer.jupyter.org/)上呈现交互式小部件

如果你的笔记本是通过小部件菜单中的"保存笔记本小部件状态"特殊操作来保存的，那么在笔记本中显示的交互式小部件也应该在nbviewer上呈现。

例如，可以查看文档中的[小部件列表](http://nbviewer.jupyter.org/github/jupyter-widgets/ipywidgets/blob/main/docs/source/examples/Widget%20List.ipynb)示例。

## 自定义小部件库的情况

自定义小部件也可以在nbviewer、静态HTML和RTD文档上呈现。一个示例是http://jupyter.org/widgets画廊。

小部件嵌入器默认尝试从npm CDN https://cdn.jsdelivr.net/npm获取自定义小部件的模型和视图实现。例如，对于`bqplot`模块名称，请求的URL带有semver范围`^2.0.0`是：

`https://cdn.jsdelivr.net/npm/bqplot@^2.0.0/dist/index.js`

其中包含了bqplot库的webpack包。

虽然默认CDN使用的是https://cdn.jsdelivr.net/npm，但可以通过设置加载`embed-amd.js`的脚本标签的可选`data-jupyter-widgets-cdn`属性来配置。

虽然默认策略是从同一个站点加载模块，然后回退到CDN。但这可以通过设置加载`embed-amd.js`的脚本标签的可选`data-jupyter-widgets-cdn-only`属性来配置。

[widget-cookiecutter](https://github.com/jupyter/widget-cookiecutter)模板项目包含了一个遵循编写小部件的最佳实践的自定义小部件库模板项目，确保你的自定义小部件库可以在nbviewer上呈现。

## 在网络环境中使用`jupyter-widgets-controls`

核心的`jupyter-widgets-controls`库，即ipywidgets的JavaScript包，对其使用的上下文（Notebook、JupyterLab、静态网页）不可知。对于每种上下文，我们都专门化了在`@jupyter-widgets/base`中实现的基础小部件管理器，以提供以下逻辑：

- 小部件应该在哪里显示，
- 如何检索有关它们状态的信息。

具体来说：

- `widgetsnbextension` Python包为经典的Jupyter笔记本提供了一个专门的小部件管理器的实现，以及作为笔记本扩展的打包逻辑。
- `@jupyter-widgets/jupyterlab-manager` npm包为`JupyterLab`上下文提供了一个专门的小部件管理器的实现，以及作为lab扩展的打包逻辑。
- 在`@jupyter-widgets/html-manager` npm包中实现的嵌入管理器是用于静态嵌入小部件的基础小部件管理器的专门化，被`Sphinx`扩展、`nbviewer`和上述讨论的"嵌入小部件"命令所使用。

我们提供了[额外的示例](https://github.com/jupyter-widgets/ipywidgets/tree/main/examples)，这些示例是基础小部件管理器专门化的其他用法，用于网络环境中的Jupyter小部件。

1. [`web1`](https://github.com/jupyter-widgets/ipywidgets/tree/main/examples/web1)示例是一个简化的示例，展示了在网络环境中使用Jupyter小部件。
2. [`web2`](https://github.com/jupyter-widgets/ipywidgets/tree/main/examples/web2)示例是一个简单的示例，利用了`application/vnd.jupyter.widget-state+json` mime类型。
3. [`web3`](https://github.com/jupyter-widgets/ipywidgets/tree/main/examples/web3)示例展示了如何在笔记本或jupyterlab上下文之外的网络环境中与Jupyter内核进行通信。
4. [`web4`](https://github.com/jupyter-widgets/ipywidgets/tree/main/examples/web4)示例展示了如何使用HTML小部件管理器在HTML文档中嵌入小部件。