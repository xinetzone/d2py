from invoke import Collection

from . import docs
from . import release

def site(name='docs', target='output/html'):
    if name == 'docs':
        out = ''
    else:
        out = name
    _config = {"sphinx": {
        "source": name,
        "target": f"{target}/{out}"
    }}
    namespace = Collection()
    namespace.add_collection(release)
    namespace.add_collection(docs)
    namespace.collections['docs'].configure(_config)
    return namespace