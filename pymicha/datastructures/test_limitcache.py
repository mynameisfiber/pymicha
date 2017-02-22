from . import LimitedCache


def test_limitcache():
    lc = LimitedCache(10)
    for i in range(15):
        lc[i] = True
    assert all(i not in lc for i in range(5))
    assert all(i in lc for i in range(5, 15))
