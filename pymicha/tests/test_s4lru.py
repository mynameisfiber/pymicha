from ..datastructures import S4LRU


def test_s4lru():
    cs = 12
    s4lru = S4LRU(cs, use_more='mem')
    for i in range(2*cs):
        s4lru[i] = i
        s4lru.get(0)
    assert all(i not in s4lru for i in range(1, cs+1))
    assert 0 in s4lru
    assert all(i in s4lru for i in range(cs+1, 2*cs))
    assert len(s4lru) == cs


def test_s4lru_mem():
    cs = 12
    s4lru = S4LRU(cs, use_more='mem')
    for i in range(2*cs):
        s4lru[i] = i
    assert all(i not in s4lru for i in range(cs))
    assert all(i in s4lru for i in range(cs, 2*cs))
    assert len(s4lru) == cs
    assert all(i in s4lru for i in reversed(range(cs, 2*cs)))
    assert len(s4lru) == cs


def test_s4lru_cpu():
    cs = 12
    s4lru = S4LRU(cs, use_more='cpu')
    for i in range(2*cs):
        s4lru[i] = i
    assert all(i not in s4lru for i in range(cs))
    assert all(i in s4lru for i in range(cs, 2*cs))
    assert len(s4lru) == cs
    assert all(i in s4lru for i in reversed(range(cs, 2*cs)))
    assert len(s4lru) == cs
