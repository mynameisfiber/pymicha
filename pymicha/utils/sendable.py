#!/usr/bin/env python

from itertools import repeat
from collections import deque


class Sendable(object):
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
    iterable = iter(iterable)
    _sendable = Sendable(iterable)
    yield from zip(repeat(_sendable.send), _sendable)
