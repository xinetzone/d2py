import setuptools
from d2py import __version__

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="d2py",  # Replace with your own username
    version=__version__,
    author="Xinwei Liu",
    author_email="735613050@qq.com",
    description="Dive into Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xinetzone/d2py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: POSIX :: Linux"
    ],
    python_requires='>=3.7',
)

