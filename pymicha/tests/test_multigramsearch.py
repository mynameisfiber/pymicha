from ..datastructures import MultigramSearch


def test_multigramsearch():
    mgs = MultigramSearch([("a", "b", "c"),
                           ("o", "c", "z"),
                           ("z", "y")])
    result = list(mgs.intersection("hello world you a b c foo".split(" ")))
    assert result == [['a', 'b', 'c']]

    result = list(mgs.intersection("hello z y world you a b c foo".split(" ")))
    assert result == [['z', 'y'], ['a', 'b', 'c']]

    result = list(mgs.intersection("hello z world you a b foo".split(" ")))
    assert result == []
