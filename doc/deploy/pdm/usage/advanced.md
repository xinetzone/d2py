# 高级用法

## 自动测试

### Use Tox as the runner

[Tox](https://tox.readthedocs.io/en/latest/) is a great tool for testing against multiple Python versions or dependency sets.
You can configure a `tox.ini` like the following to integrate your testing with PDM:

```ini
[tox]
env_list = py{36,37,38},lint
isolated_build = true

[testenv]
setenv =
    PDM_IGNORE_SAVED_PYTHON="1"
deps = pdm
commands =
    pdm install --dev
    pytest tests

[testenv:lint]
deps = pdm
commands =
    pdm install -G lint
    flake8 src/
```

To use the virtualenv created by Tox, you should make sure you have set `pdm config python.use_venv true`. PDM then will install
dependencies from [`pdm lock`](cli_reference.md#exec-0--lock) into the virtualenv. In the dedicated venv you can directly run tools by `pytest tests/` instead
of `pdm run pytest tests/`.

You should also make sure you don't run `pdm add/pdm remove/pdm update/pdm lock` in the test commands, otherwise the [`pdm lock`](cli_reference.md#exec-0--lock)
file will be modified unexpectedly. Additional dependencies can be supplied with the `deps` config. Besides, `isolated_buid` and `passenv`
config should be set as the above example to make PDM work properly.

To get rid of these constraints, there is a Tox plugin [tox-pdm](https://github.com/pdm-project/tox-pdm) which can ease the usage. You can install it by

```bash
pip install tox-pdm
```

Or,

```bash
pdm add --dev tox-pdm
```

And you can make the `tox.ini` much tidier as following, :

```ini
[tox]
env_list = py{36,37,38},lint

[testenv]
groups = dev
commands =
    pytest tests

[testenv:lint]
groups = lint
commands =
    flake8 src/
```

See the [project's README](https://github.com/pdm-project/tox-pdm) for a detailed guidance.

### Use Nox as the runner

[Nox](https://nox.thea.codes/) is another great tool for automated testing. Unlike tox, Nox uses a standard Python file for configuration.

It is much easier to use PDM in Nox, here is an example of `noxfile.py`:

```python hl_lines="4"
import os
import nox

os.environ.update({"PDM_IGNORE_SAVED_PYTHON": "1"})

@nox.session
def tests(session):
    session.run('pdm', 'install', '-G', 'test', external=True)
    session.run('pytest')

@nox.session
def lint(session):
    session.run('pdm', 'install', '-G', 'lint', external=True)
    session.run('flake8', '--import-order-style', 'google')
```

Note that `PDM_IGNORE_SAVED_PYTHON` should be set so that PDM can pick up the Python in the virtualenv correctly. Also make sure `pdm` is available in the `PATH`.
Before running nox, you should also ensure configuration item `python.use_venv` is true to enable venv reusing.

### 关于 PEP 582 `__pypackages__` 目录

By default, if you run tools by [`pdm run`](cli_reference.md#exec-0--run), `__pypackages__` will be seen by the program and all subprocesses created by it. This means virtual environments created by those tools are also aware of the packages inside `__pypackages__`, which result in unexpected behavior in some cases.
For `nox`, you can avoid this by adding a line in `noxfile.py`:

```python
os.environ.pop("PYTHONPATH", None)
```

For `tox`, `PYTHONPATH` will not be passed to the test sessions so this isn't going to be a problem. Moreover, it is recommended to make `nox` and `tox` live in their own pipx environments so you don't need to install for every project. In this case, PEP 582 packages will not be a problem either.

## 在持续集成中使用 PDM

只有一件事要记住 —— PDM 不能安装在 Python < 3.7，所以如果你的项目要在这些 Python 版本上测试，你必须确保 PDM 安装在正确的 Python 版本上，该版本可能与特定作业/任务运行的目标 Python 版本不同。

幸运的是，如果你正在使用 GitHub Action，有 [pdm-project/setup-pdm](https://github.com/marketplace/actions/setup-pdm) 可以让这个过程更容易。下面是 GitHub Actions 的工作流示例，您可以将其用于其他 CI 平台。

```yaml
Testing:
  runs-on: ${{ matrix.os }}
  strategy:
    matrix:
      python-version: [3.7, 3.8, 3.9, '3.10']
      os: [ubuntu-latest, macOS-latest, windows-latest]

  steps:
    - uses: actions/checkout@v3
    - name: Set up PDM
      uses: pdm-project/setup-pdm@v2
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        pdm sync -d -G testing
    - name: Run Tests
      run: |
        pdm run -v pytest tests
```

```{important}
对于 GitHub Action 用户，Ubuntu 虚拟环境存在 [已知兼容性问题](https://github.com/actions/virtual-environments/issues/2803)。如果 PDM 并行安装在该机器上失败，您应该将 `parallel_install` 设置为 `false` 或设置 env `LD_PRELOAD=/lib/x86_64-linux-gnu/libgcc_s.so.1`。
```

````{note}
如果运行 CI 脚本时没有适当的用户集，那么在 PDM 尝试创建其缓存目录时可能会出现权限错误。要解决这个问题，你可以自己设置 HOME 环境变量，到一个可写目录，例如：
```bash
export HOME=/tmp/home
```
````

## 在多阶段 Dockerfile 中使用 PDM

可以在多阶段 Dockerfile 中使用 PDM，首先将项目和依赖项安装到 `__pypackages__` 中。然后将该文件夹复制到最后阶段，并将其添加到 `PYTHONPATH` 中。

```dockerfile
# build stage
FROM python:3.8 AS builder

# install PDM
RUN pip install -U pip setuptools wheel
RUN pip install pdm

# copy files
COPY pyproject.toml pdm.lock README.md /project/
COPY src/ /project/src

# install dependencies and project into the local packages directory
WORKDIR /project
RUN mkdir __pypackages__ && pdm install --prod --no-lock --no-editable


# run stage
FROM python:3.8

# retrieve packages from build stage
ENV PYTHONPATH=/project/pkgs
COPY --from=builder /project/__pypackages__/3.8/lib /project/pkgs

# set command/entrypoint, adapt to fit your needs
CMD ["python", "-m", "project"]
```

## Integrate with other IDE or editors
### Work with lsp-python-ms in Emacs

Below is a sample code snippet showing how to make PDM work with [lsp-python-ms](https://github.com/emacs-lsp/lsp-python-ms) in Emacs. Contributed by [@linw1995](https://github.com/pdm-project/pdm/discussions/372#discussion-3303501).

```emacs-lisp
  ;; TODO: Cache result
  (defun linw1995/pdm-get-python-executable (&optional dir)
    (let ((pdm-get-python-cmd "pdm info --python"))
      (string-trim
       (shell-command-to-string
        (if dir
            (concat "cd "
                    dir
                    " && "
                    pdm-get-python-cmd)
          pdm-get-python-cmd)))))

  (defun linw1995/pdm-get-packages-path (&optional dir)
    (let ((pdm-get-packages-cmd "pdm info --packages"))
      (concat (string-trim
               (shell-command-to-string
                (if dir
                    (concat "cd "
                            dir
                            " && "
                            pdm-get-packages-cmd)
                  pdm-get-packages-cmd)))
              "/lib")))

  (use-package lsp-python-ms
    :ensure t
    :init (setq lsp-python-ms-auto-install-server t)
    :hook (python-mode
           . (lambda ()
               (setq lsp-python-ms-python-executable (linw1995/pdm-get-python-executable))
               (setq lsp-python-ms-extra-paths (vector (linw1995/pdm-get-packages-path)))
               (require 'lsp-python-ms)
               (lsp))))  ; or lsp-deferred
```

(pdm:hooks-for-pre-commit)=
## Hooks for `pre-commit`

[`pre-commit`](https://pre-commit.com/) is a powerful framework for managing git hooks in a centralized fashion. PDM already uses `pre-commit` [hooks](https://github.com/pdm-project/pdm/blob/main/.pre-commit-config.yaml) for its internal QA checks. PDM exposes also several hooks that can be run locally or in CI pipelines.

### Export `requirements.txt` or `setup.py`

This hook wraps the command `pdm export` along with any valid argument. It can be used as a hook (e.g., for CI) to ensure that you are going to check in the codebase a `requirements.txt` or a `setup.py` file, which reflects the actual content of [`pdm lock`](cli_reference.md#exec-0--lock).

```yaml
# export python requirements
- repo: https://github.com/pdm-project/pdm
  rev: 2.x.y # a PDM release exposing the hook
  hooks:
    - id: pdm-export
      # command arguments, e.g.:
      args: ['-o', 'requirements.txt', '--without-hashes']
      files: ^pdm.lock$
```

### Check `pdm.lock` is up to date with pyproject.toml

This hook wraps the command `pdm lock --check` along with any valid argument. It can be used as a hook (e.g., for CI) to ensure that whenever `pyproject.toml` has a dependency added/changed/removed, that `.pdm.lock` is also up to date.

```yaml
- repo: https://github.com/pdm-project/pdm
  rev: 2.x.y # a PDM release exposing the hook
  hooks:
    - id: pdm-lock-check
```
