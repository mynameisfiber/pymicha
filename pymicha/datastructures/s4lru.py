from collections import OrderedDict
from functools import wraps


def s4lru_cache(cache_size, levels=4, use_more='mem'):
    def decorator(fxn):
        kwd_mark = object()
        s4lru = S4LRU(cache_size, levels=levels,
                      use_more=use_more)

        @wraps(fxn)
        def _(*args, **kwargs):
            key = args + (kwd_mark,) + tuple(sorted(kwargs.items()))
            try:
                return s4lru.get(key)
            except KeyError:
                result = fxn(*args, **kwargs)
                s4lru.put(key, result)
                return result
        return _
    return decorator


class S4LRU(object):
    """
    Short and Simple [S4LRU][1]cache.  Implemented by Micha Gorelick
    (http://github.com/mynameisfiber) and released under the do whatever you
    want license.

    [1] http://www.cs.cornell.edu/~qhuang/papers/sosp_fbanalysis.pdf
    """
    def __init__(self, cache_size, levels=4, use_more='mem'):
        assert cache_size % levels == 0
        assert use_more in ('mem', 'cpu')
        self.cache_size = cache_size
        self.last_level = levels - 1
        self.level_size = cache_size // levels
        self.queue_levels = [OrderedDict() for i in range(levels)]
        if use_more == 'mem':
            self.lookup = dict()
        elif use_more == 'cpu':
            self.lookup = Lookup(self.queue_levels)

    def __len__(self):
        return len(self.lookup)

    def get(self, key):
        level = self.lookup.get(key, None)
        if level is not None:
            value = self._upgrade(key, level=level)
            return value
        else:
            raise KeyError(key)

    def __getitem__(self, key):
        return self.get(key)

    def __contains__(self, key):
        try:
            self.get(key)
            return True
        except KeyError:
            return False

    def put(self, key, value):
        level = self.lookup.get(key, None)
        if level is not None:
            self._upgrade(key, level)
        else:
            new_level = self.last_level
            self.queue_levels[new_level][key] = value
            self.lookup[key] = new_level
            self._clean_level(new_level, -1)

    def __setitem__(self, key, value):
        return self.put(key, value)

    def _upgrade(self, key, level=None):
        level = level or self.lookup[key]
        value = self.queue_levels[level].pop(key)
        if level == 0:
            self.queue_levels[0][key] = value
        else:
            cur_level = level - 1
            self.queue_levels[cur_level][key] = value
            self.lookup[key] = cur_level
            self._clean_level(cur_level, +1)
        return value

    def _clean_level(self, level, direction):
        num_moved = 0
        if len(self.queue_levels) <= level:
            return
        while len(self.queue_levels[level]) > self.level_size:
            key, value = self.queue_levels[level].popitem(False)
            if 0 <= level+direction < len(self.queue_levels):
                self.queue_levels[level+direction][key] = value
                self.lookup[key] = level+direction
                num_moved += 1
            else:
                self.lookup.pop(key)
        if level and num_moved:
            self._clean_level(level-1, direction)


class Lookup(object):
    def __init__(self, queue_levels):
        self.queue_levels = queue_levels

    def get(self, key, default=None):
        for i, level in enumerate(self.queue_levels):
            if key in level:
                return i
        return default

    def __getitem__(self, key):
        level = self.get(key, None)
        if level is None:
            raise KeyError
        return level

    def __setitem__(self, key, value):
        pass

    def pop(self, *args, **kwargs):
        pass

    def __len__(self):
        return sum(len(level) for level in self.queue_levels)
