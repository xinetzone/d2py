from functools import wraps
from bytecode import Bytecode, Instr
import logging
from types import MethodType


class LoggedAccess:
    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        value = getattr(obj, self.private_name)
        logging.info('Accessing %r giving %r', self.public_name, value)
        return value

    def __set__(self, obj, value):
        logging.info('Updating %r to %r', self.public_name, value)
        setattr(obj, self.private_name, value)

class runtime:
    cache = {}
    is_activate = False
    variable = LoggedAccess()
    def __init__(self, func):
        self._variable = "result"
        wraps(self.transform(func))(self)
        self.ncalls = 0

    def transform(self, func):
        if not type(self).is_activate:
            return func
        type(self).cache[func.__qualname__] = []
        c = Bytecode.from_code(func.__code__)
        extra_code = [
            Instr('STORE_FAST', '_res'),
            Instr('LOAD_FAST', self.variable),
            Instr('STORE_FAST', '_value'),
            Instr('LOAD_FAST', '_res'),
            Instr('LOAD_FAST', '_value'),
            Instr('BUILD_TUPLE', 2),
            Instr('STORE_FAST', '_result_tuple'),
            Instr('LOAD_FAST', '_result_tuple'),
        ]
        c[-1:-1] = extra_code
        func.__code__ = c.to_code()
        def wrapper(*args, **kwargs):
            res, values = func(*args, **kwargs)
            type(self).cache[func.__qualname__].append((self.variable, values))
            return res
        return wrapper

    def __call__(self, *args, **kwds):
        self.ncalls += 1
        return self.__wrapped__(*args, **kwds)

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        else:
            return MethodType(self, obj)

    @classmethod
    def activate(cls):
        cls.is_activate = True

    @classmethod
    def clear(cls):
        cls.cache.clear()
