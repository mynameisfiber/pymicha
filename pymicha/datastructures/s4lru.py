from collections import OrderedDict


class S4LRU(object):
    """
    Short and Simple [S4LRU][1]cache.  Implemented by Micha Gorelick
    (http://github.com/mynameisfiber) and released under the do whatever you
    want license.

    [1] http://www.cs.cornell.edu/~qhuang/papers/sosp_fbanalysis.pdf
    """
    def __init__(self, cache_size, levels=4):
        assert cache_size % levels == 0
        self.last_level= levels - 1
        self.level_size = cache_size // levels
        self.queue_levels = [OrderedDict() for i in range(levels)]
        self.lookup = dict()

    def get(self, key):
        level = self.lookup.get(key, None)
        if level is not None:
            value = self._upgrade(key, level=level)
            return value
        else:
            raise KeyError(key)

    def put(self, key, value):
        level = self.lookup.get(key, None)
        if level is not None:
            self._upgrade(key, level)
        else:
            new_level = self.last_level
            self.queue_levels[new_level][key] = value
            self.lookup[key] = new_level
            self._clean_level(new_level)

    def _upgrade(self, key, level=None):
        level = level or self.lookup[key]
        value = self.queue_levels[level].pop(key)
        if level == 0:
            self.queue_levels[0][key] = value
        else:
            cur_level = level - 1
            self.queue_levels[cur_level][key] = value
            self.lookup[key] = cur_level
            self._clean_level(cur_level)
        return value

    def _clean_level(self, level):
        num_moved = 0
        if len(self.queue_levels) <= level:
            return
        while len(self.queue_levels[level]) > self.level_size:
            key, value = self.queue_levels[level].popitem(False)
            try:
                self.queue_levels[level+1][key] = value
                self.lookup[key] = value
                num_moved += 1
            except IndexError:
                self.lookup.pop(key)
        if num_moved:
            self._clean_level(level+1)
