"""树结构"""


class Bunch(dict):
    """将 dict 对象切片模式转换为点抽取。
    """
    def __init__(self, bunch: dict, /, **kwargs):
        super().__init__(bunch, **kwargs)
        self.__dict__ = self
