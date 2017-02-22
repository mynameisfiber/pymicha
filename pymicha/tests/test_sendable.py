from ..utils import sendable


def counter(maxcount):
    i = 0
    while i < maxcount:
        newi = yield i
        if newi is not None:
            i = newi
        i += 1


def _test(enqueue):
    for send, i in sendable(counter(25)):
        yield i
        if i % 5 == 0:
            send(i+6, enqueue=enqueue)


def test_sendable():
    assert list(_test(enqueue=True)) == [0, 7, 8, 9, 10, 17, 18, 19, 20]


def test_sendable_noenque():
    assert list(_test(enqueue=False)) == [0, 8, 9, 10, 18, 19, 20]
