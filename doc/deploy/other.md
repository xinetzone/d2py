# 其他

- [BeeWare](https://beeware.org/): Write once. Deploy everywhere.
- [Zappa](https://github.com/zappa/Zappa): Zappa makes it super easy to build and deploy server-less, event-driven Python applications (including, but not limited to, WSGI web apps) on AWS Lambda + API Gateway. Think of it as "serverless" web hosting for your Python apps. That means infinite scaling, zero downtime, zero maintenance - and at a fraction of the cost of your current deployments!

## 取决于预装的 Python

- [PEX](https://github.com/pantsbuild/pex#user-content-pex) (Python EXecutable)
- [zipapp](https://docs.python.org/3/library/zipapp.html "(在 Python v3.10)") (does not help manage dependencies, requires Python 3.5+)
- [shiv](https://github.com/linkedin/shiv#user-content-shiv) (requires Python 3)

## Anaconda

* [用 conda 构建库和应用程序](https://conda.io/projects/conda-build/en/latest/user-guide/tutorials/index.html)
* [将一个本地 Python 包过渡到 Anaconda](https://conda.io/projects/conda-build/en/latest/user-guide/tutorials/build-pkgs-skeleton.html)

## 容器化

* [AppImage](https://appimage.org/)
* [Docker](https://www.fullstackpython.com/docker.html)
* [Flatpak](https://flatpak.org/)
* [Snapcraft](https://snapcraft.io/)

## 自带内核

*   [Vagrant](https://www.vagrantup.com/)
*   [VHD](https://en.wikipedia.org/wiki/VHD_(file_format)), [AMI](https://en.wikipedia.org/wiki/Amazon_Machine_Image), and [other formats](https://docs.openstack.org/glance/latest/user/formats.html "(在 glance v23.1.0.dev19)")
*   [OpenStack](https://www.redhat.com/en/topics/openstack) - A cloud management system in Python, with extensive VM support

## 自带硬件

将你的代码嵌入到 [Adafruit](https://github.com/adafruit/circuitpython)、[MicroPython](https://micropython.org/) 或更强大的运行 Python 的硬件上，然后将其运送到数据中心或你的用户家中。他们即插即用，你就可以收工了。

## 构建工具

- [towncrier](https://towncrier.readthedocs.io/en/stable/index.html)：Towncrier 是为项目生成有用的摘要新闻文件(也称为变更日志)的实用程序。[Sphinx 插件](https://pypi.org/project/sphinxcontrib-towncrier/)