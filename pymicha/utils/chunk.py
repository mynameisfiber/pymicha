import itertools as IT


def chunk(iterable, chunk_size, return_partial=True):
    """
    Chunks up an iterable for when you want to deal with batches. When
    `return_partial=False`, we only return chunks that can have `chunk_size`
    items.

    >>> map(batch_process, chunk(data, 32))
    """
    iterable = iter(iterable)
    size_check = 1
    if not return_partial:
        size_check = chunk_size
    while True:
        items = list(IT.islice(iterable, chunk_size))
        if len(items) < size_check:
            return
        yield items
