import collections as _col
import pathlib as _pth


path = "~/.tidy3d/pf_cache"


def _cache_path(name):
    return _pth.Path(path).expanduser() / name[:3]


class _Cache:
    def __init__(self, size):
        self.size = size
        self.data = _col.OrderedDict()

    def __getitem__(self, key):
        value = self.data.get(key, None)
        if value is not None:
            self.data.move_to_end(key)
        return value

    def __setitem__(self, key, value):
        if key in self.data:
            self.data.move_to_end(key)
        self.data[key] = value
        if self.size > 0:
            while len(self.data) >= self.size:
                self.data.popitem(False)

    def clear(self):
        self.data = _col.OrderedDict()
