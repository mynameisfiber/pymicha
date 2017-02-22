from . import chunk


def test_chunk_partial():
    items = list(range(5))
    chunked = list(chunk(items, 2, return_partial=True))
    assert chunked == [[0, 1], [2, 3], [4]]


def test_chunk_no_partial():
    items = list(range(5))
    chunked = list(chunk(items, 2, return_partial=False))
    assert chunked == [[0, 1], [2, 3]]
