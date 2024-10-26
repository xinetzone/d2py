from pathlib import Path
import logging
import sys
if sys.platform == 'win32':
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# import ablog
ROOT = Path(__file__).resolve().parents[1]
sys.path.extend([str(ROOT/'src'), str(ROOT/'doc'), str(ROOT/'doc/_ext')])
from _head import *
# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    '_build', 'Thumbs.db', 
    '.DS_Store', "_contents", 
    "**/my_notebook.ipynb",
    
]
execution_excludepatterns = ["**/my_notebook.ipynb", "multigrid", "gym", "tf",]
# 如果你希望stderr和stdout中的每个输出都被合并成一个流，请使用以下配置。
# 避免将 jupter 执行报错的信息输出到 cmd
nb_merge_streams = True
nb_execution_allow_errors = True
nb_execution_mode = "off" # "cache", "off"
# nbsphinx_assume_equations = False

logger = logging.getLogger(project)
# def source_read_handler(app, docname, source):
#     logger.info(f'{app}: {docname} -> {source}')

# def setup(app):
#     app.connect('source-read', source_read_handler)

def skip_submodules(app, what, name, obj, skip, options):
    # if what == "module":
    #     if name in ['d2py.timeitx']:
    #         skip = True
    # if what == "package":
    #     if name in ['d2py.utils']:
    #         skip = True
    if 'd2py.utils' in name or 'd2py.timeitx' in name or "d2py.analysis" in name:
        skip = True
    # logging.debug(f"skip_submodules: {what, name, obj, skip, options}")
    return skip


def setup(app):
    # from sphinx.ext.autodoc import cut_lines
    # app.connect('autodoc-process-docstring', cut_lines(4, what=['module']))
    app.add_object_type(
        "label",
        "label",
        objname="label value",
        indextemplate="pair: %s; label value",
    )
    app.connect("autoapi-skip-member", skip_submodules)

