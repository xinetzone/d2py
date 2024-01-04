"""OpenXML Document Sphinx builder.
"""
from os import path

from collections.abc import Iterable, Sequence
from docutils import nodes
from docutils.io import StringOutput
from sphinx.builders import Builder
from sphinx.util.osutil import ensuredir, os_path
from sphinx.util.nodes import inline_all_toctrees
from sphinx.util import logging
from sphinx.util.console import bold, darkgreen, brown
from .writer import DocxWriter

logger = logging.getLogger(__name__)


class DocxBuilder(Builder):
    """从 reST 源构建目标格式
    """
    name = 'docx' # 用于 `-b` 命令行选项的生成器名称。
    format = 'docx' # 生成器的输出格式，如果没有产生文档输出则为空字符串。
    epilog = '' # 在成功构建完成后发出的信息。这可以是带有以下键的 printf 样式模板字符串：``outdir``，``project``
    # 构建器的默认翻译器类。这可以通过覆盖 :py:meth:`~sphinx.application.Sphinx.set_translator` 方法来更改。
    default_translator_class: type[nodes.NodeVisitor]
    out_suffix = '.docx'

    def init(self) -> None:
        """加载必要的模板并进行初始化。默认实现不执行任何操作。"""
        ...

    def get_outdated_docs(self) -> str | Iterable[str]:
        """返回过时的输出文件的可迭代对象，或者描述更新构建将构建的内容的字符串。

        如果构建器不输出与源文件相对应的单个文件，则在此返回字符串。
        如果它这样做了，则返回需要写入的那些文件的可迭代对象。
        """
        return 'pass'

    def get_target_uri(self, docname: str, typ: str | None = None) -> str:
        """返回文档名称的目标 URI。

        Args:
            typ: 可用于限定个别构建器链接的特性。
        """
        return ''

    def prepare_writing(self, docnames: set[str]) -> None:
        """在运行 :meth:`write_doc` 之前可以添加逻辑的地方"""
        self.writer = DocxWriter(self)

    def fix_refuris(self, tree):
        # fix refuris with double anchor
        fname = self.config.master_doc + self.out_suffix
        for refnode in tree.traverse(nodes.reference):
            if 'refuri' not in refnode:
                continue
            refuri = refnode['refuri']
            hashindex = refuri.find('#')
            if hashindex < 0:
                continue
            hashindex = refuri.find('#', hashindex + 1)
            if hashindex >= 0:
                refnode['refuri'] = fname + refuri[hashindex:]

    def assemble_doctree(self):
        master = self.config.master_doc
        tree = self.env.get_doctree(master)
        tree = inline_all_toctrees(self, set(), master, tree, darkgreen, [master])
        tree['docname'] = master
        self.env.resolve_references(tree, master, self)
        self.fix_refuris(tree)
        return tree

    def write(self, *ignored):
        docnames = self.env.all_docs

        logger.info(bold('preparing documents... '), nonl=True)
        self.prepare_writing(docnames)
        logger.info('done')

        logger.info(bold('assembling single document... '), nonl=True)
        doctree = self.assemble_doctree()
        logger.info('')
        logger.info(bold('writing... '), nonl=True)
        docname = "%s-%s" % (self.config.project, self.config.version)
        self.write_doc(docname, doctree)
        logger.info('done')

    def write_doc(self, docname: str, doctree: nodes.document) -> None:
        """最终将内容写入文件系统的地方。"""
        destination = StringOutput(encoding='utf-8')
        self.writer.write(doctree, destination)
        outfilename = f"{self.outdir}/{os_path(docname) + self.out_suffix}"
        ensuredir(path.dirname(outfilename))
        try:
            self.writer.save(outfilename)
        except (IOError, OSError) as err:
            logger.warning("error writing file %s: %s" % (outfilename, err))

    def finish(self):
        """完成构建过程。

        默认实现不执行任何操作。
        """
        ...
