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
