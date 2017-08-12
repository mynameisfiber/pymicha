import sharedmem

import multiprocessing
from multiprocessing.queues import Empty
from contextlib import contextmanager


class NumpyQueue(object):
    """
    Numpy-optimized multiprocessing queue object. Useful for sharing
    homogeneous numerical data between python processes. See
    pymicha.tests.test_numpy_queue for example usage.
    
    Benchmarks between NumpyQueue and multiprocessing.queue:
        Array shape: 2x2
            mp.queue: 0.4327036259928718
            numpyqueue: 0.53742205198796
            numpyqueue2: 0.5157967879931675
        Array shape: 128x128
            mp.queue: 1.7091998109972337
            numpyqueue: 0.9855174750118749
            numpyqueue2: 0.9052893449988915
        Array shape: 256x256
            mp.queue: 11.928916561999358
            numpyqueue: 1.832176352996612
            numpyqueue2: 1.8839863180037355
    """
    def __init__(self, shape, maxsize=128, sentinal=None, dtype='float'):
        """
        shape == shape of the data to be shared
        maxsize == number of data to queue locally before blocking new data
        sentinal == value that can be put on the queue to signal there is no
                    more data
        dtype == dtype of the shared data
        """
        self.queue = multiprocessing.Queue(maxsize=maxsize-1)
        self.locks = [multiprocessing.Lock() for _ in range(maxsize)]
        self.data = sharedmem.empty([maxsize, *shape], dtype=dtype)
        self.idx = multiprocessing.Value('i', 0)
        self.SENTINAL = sentinal
        self.maxsize = maxsize
        self.shape = shape

    def __len__(self):
        return self.maxsize

    def put(self, item, metadata=None):
        """
        Add a numpy array onto the queue. item must have the same shape as
        NumpyQueue.shape. Optionally, you can provide metadata to associate
        with this item.
        """
        if item is self.SENTINAL:
            self.queue.put((self.SENTINAL, metadata))
        else:
            with self.idx:
                idx = self.idx.value
                self.queue.put((idx, metadata))
                with self.locks[idx]:
                    self.data[idx] = item
                self.idx.value = (self.idx.value + 1) % self.maxsize

    def __iter__(self):
        """
        Iterate through the items in the queue. This will return tuples
        containing the numpy arrays and their associated metadata
        """
        while True:
            try:
                with self.get(metadata=True) as (item, meta):
                    yield item, meta
            except Empty:
                raise StopIteration

    @contextmanager
    def get(self, metadata=False):
        """
        Get the next queued numpy array. Optionally also return the metadata
        associated with the item.
        """
        idx, meta = self.queue.get()
        if idx is self.SENTINAL:
            raise Empty
        else:
            with self.locks[idx]:
                if metadata:
                    yield self.data[idx], meta
                else:
                    yield self.data[idx]
