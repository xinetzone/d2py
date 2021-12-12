from pathlib import Path


def mkdir(root):
    root = Path(root)
    if not root.exists():
        root.mkdir(mode=511, parents=True, exist_ok=True)