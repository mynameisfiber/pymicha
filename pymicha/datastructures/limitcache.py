from collections import OrderedDict


class LimitedCache(OrderedDict):
    """
    Simple dictionary caching object that limits the number of cached entries
    being stored.
    """
    def __init__(self, maxsize=250):
        self.maxsize = maxsize
        super(LimitedCache, self).__init__()

    def __setitem__(self, key, value):
        while len(self) > self.maxsize:
            self.popitem(last=False)
        super(LimitedCache, self).__setitem__(key, value)
