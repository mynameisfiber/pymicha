#!/usr/bin/env python

from itertools import repeat
from collections import deque


class _Sendable(object):
    def __init__(self, iterable):
        self.iterable = iterable
        self.queue = deque()

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.queue.pop()
        except IndexError:
            pass
        return next(self.iterable)

    def send(self, *args, enqueue=True, **kwargs):
        message = self.iterable.send(*args, **kwargs)
        if enqueue:
            self.queue.append(message)
        return message


def sendable(iterable):
    """
    When looping over an generator, it's a pain to use the `send` feature to
    push values back to the generator... this fixes that. `sendable` provides a
    `send` function to send values back to the generator. When the `enque`
    parameter is given to the `send` function, the result of the `send` will be
    the value for the next loop.

    >>> for send, item in senable(c):
            print(item)
            send(item % 5)
    """
    iterable = iter(iterable)
    _sendable = _Sendable(iterable)
    yield from zip(repeat(_sendable.send), _sendable)
