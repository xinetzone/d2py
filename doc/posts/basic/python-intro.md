
```{post} Nov 01, 2021 18:00
:category: Python
:tags: basic
:excerpt: 1
```
   
# Python 初体验

叩开 Python 的大门！

```{contents}
```

## Python 是什么？

翻译自：[BeginnersGuide/Overview][1]。

Python 是一种清晰而强大的面向对象的编程语言，可与 Perl、Ruby、Scheme 或 Java 媲美。

Python 一些值得注意的特点：

- 使用优雅的语法，使你写的程序更容易阅读。
- 它是一种易于使用的语言，使你的程序能够简单地运行。这使得 Python 成为原型开发和其他临时性编程任务的理想选择，同时不影响可维护性。
- 配有大型标准库，支持许多常见的编程任务，如连接到网络服务器，用正则表达式搜索文本，读取和修改文件。
- Python 的交互式模式使得测试简短的代码片段变得很容易。还有一个捆绑的开发环境叫 IDLE。
- 通过添加用 C 或 C++ 等编译语言实现的新模块，可以轻松地进行扩展。
- 也可以嵌入到一个应用程序中，提供一个可编程的接口。
- 可在任何地方运行，包括 [Mac OS X][2]、 [Windows][3]、 [Linux][4] 和 [Unix][4]，非官方的构建也可用于 [Android][5] 和 iOS。
- 从两种意义上说，Python 是自由软件。下载或使用 Python，或在你的应用程序中包含它，都不需要任何费用。Python 还可以自由地修改和重新发布，因为虽然语言有版权，但它在 [开源许可][6] 下可以使用。

Python 的一些编程语言特点是：

- 有多种基本数据类型可用：数字（浮点、复数和无限长度的长整数）、字符串（ASCII 和 Unicode）、列表和字典。
- Python 支持面向对象的编程，具有类和多继承性。
- 代码可以被分组为模块和包。
- 该语言支持触发和捕捉异常，从而使异常处理更加简洁。
- 数据类型是强类型和动态类型。混合不兼容的类型（例如，试图添加一个字符串和一个数字）会导致引发一个异常，因此异常会被更快地捕获。
- Python 包含高级编程功能，如生成器和列表理解。
- Python 的自动内存管理使你不必在代码中手动分配和释放内存。

请阅读 [SimplePrograms][7] 的简短程序集，其长度逐渐增加，展示了 Python 的语法和可读性。

编写 Pythonic 代码并不难 —— 但你必须习惯于（PEP）的代码风格规则。你可以在 [Pythonchecker.com][8] 这样的在线资源中测试、检查和改进你的代码风格。

[1]: https://wiki.python.org/moin/BeginnersGuide/Overview
[2]: https://www.python.org/downloads/mac-osx/
[3]: https://www.python.org/downloads/windows/
[4]: https://docs.python.org/3/using/unix.html
[5]: https://wiki.python.org/moin/Android
[6]: http://www.python.org/psf/license/
[7]: https://wiki.python.org/moin/SimplePrograms
[8]: http://pythonchecker.com/

Python的设计哲学是“优雅”、“明确”、“简单”。它的重要准则被称为“Python之禅”。在 Python 解释器内运行 ``import this`` 可以获得完整的列表（翻译为中文）：

```{epigraph}
优美优于丑陋。明了优于隐晦。

简单优于复杂。复杂优于凌乱。

扁平优于嵌套。稀疏优于稠密。

可读性很重要。
```

Python 开发者的哲学是“用一种方法，最好是只有一种方法来做一件事”。

在设计 Python 语言时，如果面临多种选择，Python 开发者一般会拒绝花俏的语法，而选择明确没有或者很少有歧义的语法。

## 为什么学习 Python？

0. 易学
1. 可读和可维护的代码
2. 与主要平台和系统兼容
3. 强大的标准库
4. 许多开源框架和工具
5. 简化复杂的软件开发

## 学习 Python 可以做什么？

翻译自：[what-can-i-do-with-python](https://realpython.com/what-can-i-do-with-python/)。

列出一些常用 Python 库。

### 做一般的软件开发

#### Web 开发

库|描述
:-|:-
[Django][21]|Django 是一个高水平的框架，它鼓励以简洁和务实的设计来快速开发 Web 应用。它允许你专注于编写你的应用程序，而不需要重新发明轮子。
[FastAPI][22]|FastAPI 是一个用于构建网络 API 的快速和高性能的网络框架。它建立在现代 Python 类型提示功能之上，并实现了[异步](https://realpython.com/async-io-python/)编程。
[Flask][23]|Flask 是一个轻量级的框架，用于创建 [WSGI](https://wsgi.readthedocs.io/) Web 应用程序。它允许你快速上手，并在需要时扩展到复杂的应用程序。
[Tornado][24]|Tornado 是一个网络框架和异步网络库。它使用非阻塞网络 [I/O](https://en.wikipedia.org/wiki/Input/output)，所以你可以编写可以扩展到数以万计的开放连接的应用程序。

[21]: https://www.djangoproject.com/
[22]: https://fastapi.tiangolo.com/
[23]: https://palletsprojects.com/p/flask/
[24]: https://www.tornadoweb.org/en/stable/

#### CLI 开发

CLI：命令行界面

库|描述
:-|:-
[argparse][33]|`argprse` 是一个[标准库](https://docs.python.org/3/library/index.html)模块，允许你编写用户友好的命令行接口。你可以定义你想在命令行中接受的参数，并很好地解析它们。它自动生成帮助和使用信息，并在你的用户提供无效的输入时发出错误。
[Click][34]|Click 是一个 Python 软件包，用于用尽可能少的代码创建漂亮的命令行界面。它具有高度的可配置性，开箱即有合理的默认值。它的目标包括使编写命令行工具的过程变得快速而有趣。
[Typer][35]|Typer 是一个用于构建 CLI 应用程序的库，用户会喜欢使用它，开发人员会喜欢创建它。它为所有[外壳](https://en.wikipedia.org/wiki/Shell_(computing))提供自动帮助信息和自动完成。它最大限度地减少了代码的重复，方便了调试。

[33]: https://docs.python.org/3/library/argparse.html#module-argparse
[34]: https://palletsprojects.com/p/click/
[35]: https://typer.tiangolo.com/

#### GUI 开发

库|描述
| --- | --- |
| [Kivy](https://kivy.org/#home) | Kivy is a library for rapid development of applications with innovative user interfaces, such as [multi-touch](https://en.wikipedia.org/wiki/Multi-touch) applications. It runs on Linux, Windows, macOS, Android, iOS, and [Raspberry Pi](https://realpython.com/python-raspberry-pi/). |
| [PyQt](https://www.riverbankcomputing.com/static/Docs/PyQt6/) | PyQt is a set of Python bindings for the [Qt](https://wiki.qt.io/About_Qt) application framework. It includes classes for building GUI applications. It also provides classes for networking, [threads](https://realpython.com/python-pyqt-qthread/), [SQL databases](https://realpython.com/python-pyqt-database/), and more. It supports the Windows, Linux, and macOS platforms. |
| [PySimpleGUI](https://pysimplegui.readthedocs.io/en/latest/) | PySimpleGUI is a library that aims to transform the tkinter, Qt, wxPython, and [Remi](https://github.com/dddomodossola/remi) GUI frameworks into a simpler interface. It uses Python core data types to define windows and simplify event handling. |
| [Qt for Python (`PySide6`)](https://www.qt.io/qt-for-python) | Qt for Python is a project that provides the official set of Python bindings (`PySide6`) for the Qt framework. |
| [tkinter](https://docs.python.org/3/library/tkinter.html#module-tkinter) | tkinter is a standard Python interface to the [Tk GUI toolkit](https://en.wikipedia.org/wiki/Tk_(software)). It allows you to build GUI applications without the need for third-party dependencies. It’s available on most Unix platforms as well as on Windows systems. |
| [wxPython](https://www.wxwidgets.org/) | wxPython is a Python binding for the [wxWidgets](https://www.wxwidgets.org/) [C++](https://en.wikipedia.org/wiki/C%2B%2B) library. It allows you to create applications for Windows, macOS, and Linux with a single code base. It gives applications a native look and feel because it uses the platform’s native [API](https://en.wikipedia.org/wiki/API). |

#### 游戏开发

| Library | Description |
| --- | --- |
| [Arcade](https://arcade.academy/index.html) | Arcade is a Python library for creating 2D video games. It’s ideal for people learning to program because they don’t need to learn a complex game framework to start creating their own games. |
| [PyGame](https://www.pygame.org/wiki/about) | PyGame is a set of Python modules designed for writing video games. It adds functionality on top of the [SDL](http://www.libsdl.org/) library. It allows you to create full-featured games and multimedia programs. The library is highly portable and runs on several platforms and operating systems. |
| [pyglet](http://pyglet.org/) | pyglet is a powerful Python library for creating games and other visually rich applications on Windows, macOS, and Linux. It supports windowing, user interface event handling, [OpenGL](https://en.wikipedia.org/wiki/OpenGL) graphics, loading images, and playing videos and music. |



### 潜心研究数据科学和数学

#### 机器学习

| Library | Description |
| --- | --- |
| [Keras](https://keras.io/) | Keras is an industrial-strength deep learning framework with an API designed for human beings. It allows you to run new experiments and try more ideas quickly. It follows best practices for reducing cognitive load. |
| [NLTK](https://www.nltk.org/) | NLTK is a platform for building Python programs to [work with human language data](https://realpython.com/nltk-nlp-python/). It provides libraries for classification, tokenization, stemming, tagging, parsing, and semantic reasoning. |
| [PyTorch](https://pytorch.org/) | PyTorch is an open source machine learning framework that accelerates the path from research prototyping to production deployment. |
| [scikit-learn](http://scikit-learn.org/) | scikit-learn is an open source machine learning library that supports [supervised](https://en.wikipedia.org/wiki/Supervised_learning) and [unsupervised learning](https://en.wikipedia.org/wiki/Unsupervised_learning). It’s an efficient tool for predictive data analysis that’s accessible to everybody and reusable in various contexts. |
| [TensorFlow](https://www.tensorflow.org/) | TensorFlow is an end-to-end open source platform for machine learning. It has a comprehensive, flexible ecosystem of tools, libraries, and community resources that will help you build and deploy ML-powered applications. |

#### 科学计算

| Library | Description |
| --- | --- |
| [NumPy](https://numpy.org/) | NumPy is a fundamental package for scientific computing with Python. It offers comprehensive mathematical functions, random number generators, linear algebra routines, Fourier transforms, and more. It provides a high-level syntax that makes it accessible and productive. |
| [SciPy](https://www.scipy.org/) | SciPy is a Python-based collection of open source software for mathematics, science, and engineering. |
| [SimPy](https://simpy.readthedocs.io/en/latest/) | SimPy is a process-based discrete-event simulation framework based on Python. It can help you simulate real-world systems, such as airports, customer services, highways, and more. |

#### 数据分析和可视化

| Library | Description |
| --- | --- |
| [Bokeh](https://bokeh.org/) | Bokeh is an interactive data visualization library for web browsers. It provides tools for constructing elegant and versatile graphics. It can help you quickly make interactive plots, dashboards, and data applications. |
| [Dash](https://plotly.com/dash/) | Dash is a Python framework for building web analytic applications quickly. It’s ideal for building data visualization applications with custom user interfaces that render in the browser. |
| [Matplotlib](https://matplotlib.org/) | Matplotlib is a library for creating static, animated, and interactive data visualizations in Python. |
| [pandas](https://pandas.pydata.org/) | pandas is a powerful and flexible open source tool for analyzing and manipulating data. It provides fast, flexible, and expressive data structures to work with relational or labeled data. |
| [Seaborn](https://seaborn.pydata.org/) | Seaborn is a Python data visualization library based on Matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics that allow you to explore and understand your data. It integrates closely with pandas data structures. |

#### 网络爬虫

| Library | Description |
| --- | --- |
| [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) | Beautiful Soup is a Python library for pulling data out of HTML and XML files into parse trees. The library provides methods and Pythonic idioms to navigate, search, modify, and extract information from parse trees. |
| [`requests`](https://docs.python-requests.org/en/master/) | `requests` is an elegant and powerful [HTTP](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol) library for Python. It provides an intuitive and concise API designed for human beings. |
| [Scrapy](https://docs.scrapy.org/en/latest/) | Scrapy is a fast, high-level web crawling and web scraping framework. It allows you to crawl websites and extract structured data from their pages. |
| [`urllib.request`](https://docs.python.org/3/library/urllib.request.html#module-urllib.request) | `urllib.request` is a standard library module that defines functions and classes to help you open URLs. It also allows you to work with basic and [digest authentication](https://en.wikipedia.org/wiki/Digest_access_authentication), redirections, cookies, and more. |

### 加快工作流程并使之自动化

#### DevOps

DevOps 包括软件开发和一般 [IT运营](https://en.wikipedia.org/wiki/IT_operations)。DevOps 允许你处理你的应用程序和软件产品的整个生命周期。它包括开发、测试、打包和部署，以及其他相关操作。

| Library | Description |
| --- | --- |
| [Ansible](https://www.ansible.com/) | Ansible is a tool for software [provisioning](https://en.wikipedia.org/wiki/Provisioning), configuration management, and [application deployment](https://en.wikipedia.org/wiki/Application_deployment). It enables [infrastructure as code](https://en.wikipedia.org/wiki/Infrastructure_as_code). |
| [Docker Compose](https://docs.docker.com/compose/) | Docker Compose is a tool for defining and running multicontainer [Docker](https://docs.docker.com/) applications. You can configure your application’s services with a [YAML](https://yaml.org/) file. Then, with a single command, you can create and start all the services from your configuration file. It works on production, staging, development, testing, and more. |

To get started with DevOps, check out:

*   [Python DevOps Tutorials](https://realpython.com/tutorials/devops/)
*   [DevOps With Python Learning Path](https://realpython.com/learning-paths/python-devops/)

#### 开发环境

为你和你的队友构建一个高效的环境是软件开发的一个基本部分。为此，Python 有一套很好的工具，允许你在每个项目的虚拟环境中隔离你的包、库和 Python 版本。

| 工具 | 描述 |
| --- | --- |
| [`conda`](https://docs.conda.io/en/latest/) | `conda` 是一个开源的软件包和环境管理系统。它允许你快速安装、运行和更新软件包及其依赖关系。它帮助你寻找和安装软件包。|
| [`pip`](https://pip.pypa.io/en/stable/) |  `pip`是一个[Python 的软件包管理工具](https://packaging.python.org/guides/tool-recommendations/)。它允许你从 [PyPI](https://pypi.org/) 和其他索引中安装软件包。 |
| [Pipenv](https://pipenv.pypa.io/en/latest/) | `Pipenv` 是一个旨在为 Python 世界带来所有打包世界中最好的工具。它允许你为你的项目创建和管理虚拟环境。它提供了一种通过统一接口一起使用 `pip` 和 [`virtualenv`](https://virtualenv.pypa.io/en/latest/) 的方法。 |
| [pipx](https://pipxproject.github.io/pipx/) | `pipx` 是一个帮助你在隔离环境中安装和运行用 Python 编写的终端用户应用程序的工具。它为每个应用程序及其相关的软件包创建一个隔离的环境。它使应用程序在你的命令行或 shell 中可用。|
| [pyenv](https://github.com/pyenv/pyenv) | `pyenv` 是一个用于安装和管理多个 Python 版本的工具。它可以让你在它们之间快速切换。它还允许你定义每个项目的 Python 版本。 |

要建立一个有效的开发环境，请查看。

#### 软件打包与部署

软件开发周期的另一个关键部分是打包、分发和部署你的产品给你的终端用户或客户。在 Python 中，部署应用程序和库的一个快速而流行的方法是将它们发布到 PyPI。

| Tool | Description |
| --- | --- |
| [Flit](https://flit.readthedocs.io/en/latest/index.html) | Flit is a tool that provides a quick way to put your Python packages and modules on PyPI. It helps you set up the information about your package, so you can publish it to PyPI with minimal effort. |
| [Poetry](https://python-poetry.org/) | Poetry is a tool for creating, building, installing, and packaging Python projects. It also allows you to publish your projects to PyPI. It tracks and resolves your project’s dependencies. It uses your current virtual environments or creates new ones to isolate your packages from your system-wide Python installation. |
| [PyInstaller](https://www.pyinstaller.org/) | PyInstaller is a tool that freezes Python applications into stand-alone executables that work under Windows, GNU/Linux, macOS, and others. |
| [setuptools](https://packaging.python.org/key_projects/#setuptools) | setuptools is a collection of enhancements to the Python [distutils](https://packaging.python.org/key_projects/#distutils) that allows you to build and distribute Python [distributions](https://packaging.python.org/glossary/#term-Distribution-Package), especially those that depend on other packages. |
| [Twine](https://twine.readthedocs.io/en/latest/) | Twine is a utility for publishing Python packages on PyPI. It allows you to upload source and binary distributions of your projects. |

To get started, check out:

*   [How to Publish an Open Source Python Package to PyPI](https://realpython.com/pypi-publish-python-package/)
*   [Using PyInstaller to Easily Distribute Python Applications](https://realpython.com/pyinstaller-python/)

With these resources, you can get started with packaging and deploying your Python applications, libraries, and packages to your end users, clients, and colleges. Also, the [Python Packaging Authority](https://packaging.python.org/) provides a lot of useful information and tutorials to help you distribute Python packages with modern tools.

#### 数据库系统

| Library | Database | Description |
| --- | --- | --- |
| [MongoEngine](http://docs.mongoengine.org/) | [MongoDB](https://realpython.com/introduction-to-mongodb-and-python/) | MongoEngine is a document-object mapper for working with MongoDB using object-oriented programming in Python. |
| [MySQL Connector/Python](https://dev.mysql.com/doc/connector-python/en/) | [MySQL](https://dev.mysql.com/) | MySQL Connector is a self-contained Python driver for communicating with MySQL servers. |
| [Psycopg](https://www.psycopg.org/) | [PostgreSQL](https://www.postgresql.org/about/) | Psycopg is a PostgreSQL database adapter for the Python programming language. |
| [PyMongo](https://pymongo.readthedocs.io/en/stable/index.html) | [MongoDB](https://docs.mongodb.com/) | PyMongo is a Python distribution containing tools for working with MongoDB databases. It provides a native Python driver for this type of database system. |
| [SQLAlchemy](https://www.sqlalchemy.org/) | [SQL](https://realpython.com/python-sql-libraries/) | SQLAlchemy is a Python SQL toolkit and object-relational mapper for SQL databases. |
| [`sqlite3`](https://docs.python.org/3/library/sqlite3.html#module-sqlite3) | [SQLite](https://www.sqlite.org/about.html) | `sqlite3` is a lightweight disk-based database that doesn’t require a separate server process. It allows you to access databases using a nonstandard variant of SQL. It’s freely available and comes in the Python standard library. |

To get started with databases, check out:

*   [Python Database Tutorials](https://realpython.com/tutorials/databases/)
*   [Data Collection & Storage Learning Path](https://realpython.com/learning-paths/data-collection-storage/)

Creating and working with databases is a powerful way to manage data in your Python applications. Databases add significant functionality and versatility to your programs and allow you to provide exciting features to your users and client. Managing databases is a fundamental skill in your developer education.

#### 软件测试

| Tool | Description |
| --- | --- |
| [doctest](https://docs.python.org/3/library/doctest.html#module-doctest) | doctest is a standard module that searches your [docstrings](https://realpython.com/documenting-python-code/) for pieces of text that look like [interactive Python sessions](https://realpython.com/interacting-with-python/) and executes them to verify that they work correctly. |
| [pytest](https://docs.pytest.org/en/6.2.x/contents.html) | pytest is a robust and mature testing framework that allows you to write and automate tests. It can scale from small unit tests to complex functional tests for your applications and libraries. |
| [tox](https://tox.readthedocs.io/en/latest/) | tox is a generic [virtualenv](https://pypi.org/project/virtualenv) management and test command-line tool. It allows you to check if your packages install correctly within different Python versions and interpreters. It can run your tests in each of the configured environments. |
| [`unittest`](https://docs.python.org/3/library/unittest.html#module-unittest) | `unittest` is a unit testing framework available in the Python standard library. It supports test automation, setup and teardown of tests, aggregation of tests into collections, and more. |

To get started with testing, check out:

*   [Python Testing Tutorials](https://realpython.com/tutorials/testing/)
*   [Test Your Python Apps Learning Path](https://realpython.com/learning-paths/test-your-python-apps/)

As a developer, you need to produce reliable code that works correctly. This means that you need to test your code every time you change it or add new features. Automated tests are the way to go in these situations.

### 构建嵌入式系统和机器人

随着科学技术的发展，物联网、家庭自动化、自动驾驶汽车和机器人等领域已经变得越来越流行。

| Library | Description |
| --- | --- |
| [BBC micro:bit](https://microbit.org/) | BBC micro:bit is a pocket-sized computer that introduces you to how software and hardware work together. It is programmable with Python. |
| [CircuitPython](https://circuitpython.org/) | CircuitPython is a programming language designed to simplify experimenting and learning to code on low-cost microcontroller boards. |
| [MicroPython](https://micropython.org/) | MicroPython is a lean and efficient implementation of Python. It includes a small subset of the Python standard library. It’s optimized to run on microcontrollers and in constrained environments. |
| [PythonRobotics](https://atsushisakai.github.io/PythonRobotics/) | PythonRobotics is a compilation of various robotics algorithms with visualizations. It’s focused on autonomous navigation. Its goal is to allow you to understand the basic ideas behind each robotic algorithm it provides. |
| [Raspberry Pi](https://www.raspberrypi.org/about/) | Raspberry Pi is a general-purpose, Linux-based computer. It has a complete operating system with a GUI interface that is capable of running many different programs at the same time. Python comes built in on the Raspberry Pi. |
| [rospy](http://wiki.ros.org/rospy) | rospy is a client library for [ROS (Robot Operating System)](https://www.ros.org/). Its API enables Python programmers to quickly interface with ROS to create complex and reliable robot behaviors. |

To get started with embedded Python, check out:

*   [MicroPython: An Intro to Programming Hardware in Python](https://realpython.com/micropython/)
*   [Episode 5: Exploring CircuitPython](https://realpython.com/podcasts/rpp/5/)
*   [Embedded Python: Build a Game on the BBC micro:bit](https://realpython.com/embedded-python/)

If you want to start creating a hardware-related project with Python, then look at how to build [physical projects with Python on the Raspberry Pi](https://realpython.com/python-raspberry-pi/). In this project, you’ll learn how to set up a Raspberry Pi, run Python code on it, read input from its sensors, send signals to its electronic components, and more.


