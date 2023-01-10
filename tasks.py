import inspect

if not hasattr(inspect, 'getargspec'): # 修复
    inspect.getargspec = inspect.getfullargspec
    
from d2py.tools.write import site

namespace = site('doc', target='doc/_build/html')
