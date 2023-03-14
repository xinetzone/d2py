from collections import UserDict


class Bunch(UserDict):
    """将 dict 对象切片模式转换为点抽取。
    """
    def __init__(self, dict=None, /, **kwargs):
        super().__init__(dict, **kwargs)
        self.__dict__ = self
