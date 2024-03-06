from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def mkdir(root: str|Path):
    """创建文件夹"""
    root = Path(root)
    if not root.exists():
        root.mkdir(mode=511, parents=True, exist_ok=True)
        logger.info(f"{root} 创建成功")
    else:
        logger.info(f"{root} 已存在无需创建")
