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
logger = logging.getLogger(project)
# def source_read_handler(app, docname, source):
#     logger.info(f'{app}: {docname} -> {source}')

# def setup(app):
#     app.connect('source-read', source_read_handler)

# jupyterlite_dir = ROOT/"tools/lite/apps"
def setup(app):
    # from sphinx.ext.autodoc import cut_lines
    # app.connect('autodoc-process-docstring', cut_lines(4, what=['module']))
    app.add_object_type(
        "label",
        "label",
        objname="label value",
        indextemplate="pair: %s; label value",
    )

# suppress_warnings = ["myst.xref_missing"]
jupyterlite_contents = f"{ROOT}/tests/lite_contents"
jupyterlite_bind_ipynb_suffix = False