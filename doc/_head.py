import d2py
from d2py.utils.log_config import config_logging
# -- Project information -----------------------------------------------------

project = 'd2py'
copyright = '2021, xinetzone'
author = 'xinetzone'

# The full version, including alpha/beta/rc tags
release = d2py.__version__
html_baseurl = 'https://xinetzone.github.io/d2py'
# 配置日志信息
config_logging(f"{project}.log", project)

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    # "IPython.sphinxext.ipython_console_highlighting",
    "ablog",
    "sphinx.ext.graphviz",
    "myst_nb",
    # "nbsphinx",  
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx_thebe",
    "sphinx_copybutton",
    "sphinx_comments",
    "sphinxcontrib.mermaid",
    "matplotlib.sphinxext.plot_directive",
    "sphinx_plotly_directive",
    "sphinx_sitemap",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx_automodapi.automodapi",
    "sphinx_automodapi.smart_resolver",
    'autoapi.extension',
    "sphinxcontrib.bibtex",
    "sphinx.ext.viewcode",
    # "sphinx.ext.doctest",
    "sphinx_design",
    # "sphinx_packaging",
    "sphinxcontrib.mermaid",
    # "sphinx.ext.ifconfig",
    # "sphinx_immaterial",
    "code_annotations",
    # "sphinx.ext.todo",
    "todo",
    # "sphinxext.opengraph",
    # "sphinx_docx",
    "helloworld",
    # for pretty schema
    # "sphinx-jsonschema",
    'sphinx.ext.mathjax',
    # 'jupyterlite_sphinx',
    # "sphinxcontrib.katex"
]

myst_enable_extensions = [
    "colon_fence",
    "amsmath",
    "deflist",
    "dollarmath",
    "html_admonition",
    "html_image",
    "replacements",
    "smartquotes",
    "substitution",
    "tasklist",
]

comments_config = {
    "hypothesis": True,
    "dokieli": False,
    "utterances": {
        "repo": "xinetzone/d2py",
        "optional": "config",
    }
}

# # # MyST NB 设置
# # nb_mime_priority_overrides = [
# #     ("html", "text/html", 0),
# #     ("latex", "text/latex", 20),
# #     ("html", "application/vnd.jupyter.widget-view+json", 10),
# #     # ("image", "image/svg+xml", None)
# #     # (
# #     #     ,
# #     #     "application/javascript",
# #     #     "text/html",
# #     #     "image/svg+xml",
# #     #     "image/png",
# #     #     "image/jpeg",
# #     #     "text/markdown",
# #     #     "text/latex",
# #     #     "text/plain",
# #     # ), 0)
# # ]

# extlinks = {
#     # 'duref': ('https://docutils.sourceforge.io/docs/ref/rst/'
#     #           'restructuredtext.html#%s', ''),
#     # 'durole': ('https://docutils.sourceforge.io/docs/ref/rst/'
#     #            'roles.html#%s', ''),
#     # 'dudir': ('https://docutils.sourceforge.io/docs/ref/rst/'
#     #           'directives.html#%s', ''),
#     # 'daobook': ('https://daobook.github.io/%s', ''),
# }

intersphinx_mapping = {
    "rich": ("https://rich.readthedocs.io/en/latest", None),
    "pyarrow": ("https://arrow.apache.org/docs", None),
    "ipython": ("https://ipython.readthedocs.io/en/latest/", None),
    "pytest": ("https://docs.pytest.org/en/latest/", None),
    "filesystem-spec": ("https://filesystem-spec.readthedocs.io/en/latest", None),
    "jupyter-notebook": (
        "https://jupyter-notebook.readthedocs.io/en/stable",
        None,
    ),
    "jupyterhub": ("https://jupyterhub.readthedocs.io/en/stable", None),
    "nbconvert": ("https://nbconvert.readthedocs.io/en/latest", None),
    "jupyter-contrib-nbextensions": (
        "https://jupyter-contrib-nbextensions.readthedocs.io/en/latest",
        None,
    ),
    "jupyterlite": (
        "https://jupyterlite.readthedocs.io/en/stable",
        None,
    ),
    "nbsphinx": ("https://nbsphinx.readthedocs.io", None),
    "spack": ("https://spack-tutorial.readthedocs.io/en/latest", None),
    "ipyparallel": ("https://ipyparallel.readthedocs.io/en/latest", None),
    # "bokeh": ("https://docs.bokeh.org/en/latest", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable", None),
    "pyviz": ("https://pyviz-tutorial.readthedocs.io/de/latest", None),
    "python-basics": (
        "https://python-basics-tutorial.readthedocs.io/en/latest",
        None,
    ),
    "python4datascience": (
        "https://www.python4data.science/en/latest",
        None,
    ),
    'python': ('https://daobook.github.io/cpython', None),
    'sphinx': ('https://daobook.github.io/sphinx', None),
    'peps': ('https://daobook.github.io/peps', None),
    "Fabric": ("https://docs.fabfile.org/en/latest", None),
    "Invoke": ("https://docs.pyinvoke.org/en/stable", None),
    "Paramiko": ("https://docs.paramiko.org/en/latest", None),
    "invocations": ("https://invocations.readthedocs.io/en/latest", None),
    "patchwork": ("https://fabric-patchwork.readthedocs.io/en/latest", None),
    "telnetlib3": ("https://telnetlib3.readthedocs.io/en/latest", None),
    "cppyy": ("https://cppyy.readthedocs.io/en/latest", None),
    "gymnasium": ("https://gymnasium.farama.org", None),
    "matplotlib": ("https://matplotlib.org/stable", None),
    "tensorflow": ("https://www.tensorflow.org", None),
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'zh_CN'

suppress_warnings = [
    "mystnb.unknown_mime_type",  # 禁用 application/vnd.plotly.v1+json and application/vnd.bokehjs_load.v0+json 警告
    "myst.xref_missing", # 禁用 myst 警告
    "autoapi.python_import_resolution", "autoapi.not_readable" # 禁用 autoapi 警告
]
# jupyterlite_dir = ROOT/"tools/lite/apps"
jupyterlite_contents = "../tests"
jupyterlite_bind_ipynb_suffix = False
jupyterlite_config = "jupyterlite_config.json"

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "xyzstyle"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_css_files = ["default.css", "try_examples.css"]

# -- 国际化输出 ----------------------------------------------------------------

locale_dirs = ['locales/']  # path is example but recommended.
gettext_compact = False  # optional.

extra_navbar = """<div>
版权所有 © 2021 <a href="https://xinetzone.github.io/">xinetzone</a></div>
<div>由 <a href="https://xinetzone.github.io/demo-book/">EBP</a> 提供技术支持</div>
<a href="https://d2py.readthedocs.io/zh/latest/">版本切换</a>
"""
autosummary_generate = True

html_theme_options = {
    # -- 如果你的文档只有一个页面，而且你不需要左边的导航栏，那么 ---------------
    # 你可以在 单页模式 下运行，
    # "single_page": False,  # 默认 `False`
    # 默认情况下，编辑按钮将指向版本库的根。
    # 如果你的文档被托管在一个子文件夹中，请使用以下配置：
    "path_to_docs": "doc/",  # 文档的路径，默认 `docs/``
    "github_url": "https://github.com/xinetzone/d2py",
    "repository_url": "https://github.com/xinetzone/d2py",
    "repository_branch": "main",  # 文档库的分支，默认 `master`
    # -- 在导航栏添加一个按钮，链接到版本库的议题 ------------------------------
    # （与 `repository_url` 和 `repository_branch` 一起使用）
    # -- 在导航栏添加一个按钮，以下载页面的源文件。
    # "use_download_button": True,  # 默认 `True`
    # 你可以在每个页面添加一个按钮，允许用户直接编辑页面文本，
    # 并提交拉动请求以更新文档。
    "use_edit_page_button": True,
    # 在导航栏添加一个按钮来切换全屏的模式。
    # "use_fullscreen_button": True,  # 默认 `True`
    # -- 在导航栏中添加一个链接到文档库的按钮。----------------------------------
    # "use_repository_button": True,  # 默认 `False`
    # -- 包含从 Jupyter 笔记本建立页面的 Binder 启动按钮。 ---------------------
    # "launch_buttons": '', # 默认 `False`
    "home_page_in_toc": False,  # 是否将主页放在导航栏（顶部）
    # -- 只显示标识，不显示 `html_title`，如果它存在的话。-----
    # -- 在导航栏中显示子目录，向下到这里列出的深度。 ----
    # "show_navbar_depth": 2,
    # -- 在侧边栏页脚添加额外的 HTML -------------------
    # （如果 `sbt-sidebar-footer.html `在 `html_sidebars` 中被使用）。
    # "extra_navbar": extra_navbar,
    # -- 在每个页面的页脚添加额外的 HTML。---
    # "extra_footer": '',
    # （仅限开发人员）触发一些功能，使开发主题更容易。
    # "theme_dev_mode": False
    # 重命名页内目录名称
    # "toc_title": "导航",
    "launch_buttons": {
        # https://mybinder.org/v2/gh/xinetzone/d2py/main
        "binderhub_url": "https://mybinder.org",
        # "jupyterhub_url": "https://datahub.berkeley.edu",  # For testing
        "colab_url": "https://colab.research.google.com/",
        # 你可以控制有人点击启动按钮时打开的界面。
        "notebook_interface": "jupyterlab",
        "thebe": True,  # Thebe 实时代码单元格
    },
    # 图标可以参考 https://fontawesome.com/icons
    "icon_links": [
        # {
        #     "name": "GitHub",
        #     "url": "https://github.com/xinetzone/d2py",
        #     "icon": "fa-brands fa-square-github",
        #     "type": "fontawesome",
        # },
        {
            "name": "知乎",
            "url": "https://www.zhihu.com/people/xinetzone",
            "icon": "fa-brands fa-zhihu",
            "type": "fontawesome",
        },
        {
            "name": "简书",
            "url": "https://www.jianshu.com/u/4302480a3e8e",
            "icon": "fa-solid fa-book",
            "type": "fontawesome",
        },
        {
            "name": "B站",
            "url": "https://space.bilibili.com/252192181",
            "icon": "fa-brands fa-bilibili",
            "type": "fontawesome",
        },
        {
            "name": "博客园",
            "url": "https://www.cnblogs.com/q735613050/",
            "icon": "https://xinetzone.github.io/xinetzone/media/xinetzone.jpg",
            "type": "url",
        },
        {
            "name": "领英",
            "url": "https://www.linkedin.com/in/xinet",
            "icon": "fa-brands fa-linkedin",
            "type": "fontawesome",
        }
        # {
        #     "name": "GitLab",
        #     "url": "https://gitlab.com/<your-org>/<your-repo>",
        #     "icon": "fa-brands fa-square-gitlab",
        #     "type": "fontawesome",
        # },
        # {
        #     "name": "Twitter",
        #     "url": "https://twitter.com/<your-handle>",
        #     "icon": "fa-brands fa-square-twitter",
        #     # The default for `type` is `fontawesome` so it is not actually required in any of the above examples as it is shown here
        # },
        # {
        #     "name": "Mastodon",
        #     "url": "https://<your-host>@<your-handle>",
        #     "icon": "fa-brands fa-mastodon",
        # },
    ],
    "footer_start": ["version-switcher", "copyright"],
    "footer_end": ["sphinx-version", "last-updated"],
    "navigation_with_keys": True
}
# -- 自定义网站的标志 --------------
html_logo = 'logo.jpg'
# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = "page-logo.jfif"

# -- 自定义网站的标题 --------------
# html_title = '动手学习 Python'

todo_include_todos = True

bibtex_bibfiles = ["refs.bib"]
bibtex_reference_style = "author_year"
graphviz_output_format = 'svg'

# -- epub --------------------------

# Bibliographic Dublin Core info.
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright

# -- Options for autosummary/autodoc output ------------------------------------
autosummary_generate = True
autodoc_typehints = "description"
autodoc_member_order = "groupwise"

# -- Options for autoapi -------------------------------------------------------
autoapi_type = "python"
autoapi_dirs = ["../src/d2py"]
autoapi_keep_files = True # 要开始自己编写 API 文档，你可以让 AutoAPI 保留其生成的文件作为基础
autoapi_root = "api"
autoapi_member_order = "groupwise"

# -- Options for LaTeX output --------------------------------------------------
latex_engine = "xelatex"

# Katex
katex_prerender = True
katex_css_path = \
    'https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css'
katex_js_path = 'katex.min.js'
katex_autorender_path = 'auto-render.min.js'
katex_inline = [r'\(', r'\)']
katex_display = [r'\[', r'\]']
katex_prerender = False
katex_options = r'''{
    displayMode: true,
    macros: {
        "\\RR": "\\mathbb{R}",
        "\\i": "\\mathrm{i}",
        "\\e": "\\mathrm{e}^{#1}",
        "\\vec": "\\mathbf{#1}",
        "\\x": "\\vec{x}",
        "\\d": "\\operatorname{d}\\!{}",
        "\\dirac": "\\operatorname{\\delta}\\left(#1\\right)",
        "\\scalarprod": "\\left\\langle#1,#2\\right\\rangle",
    }
}'''
