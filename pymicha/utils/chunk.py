import itertools as IT


def chunk(iterable, chunk_size, return_partial=True):
    iterable = iter(iterable)
    size_check = 1
    if not return_partial:
        size_check = chunk_size
    while True:
        items = list(IT.islice(iterable, chunk_size))
        if len(items) < size_check:
            return
        yield items
