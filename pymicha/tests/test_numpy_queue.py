import multiprocessing
import numpy as np
from ..datastructures import NumpyQueue, Empty


class TestProcessNumpyQueue(multiprocessing.Process):
    def __init__(self, slm):
        super().__init__()
        self.slm = slm

    def run(self):
        for c in range(10000):
            a = np.zeros(shape=self.slm.shape) + c
            self.slm.put(a, metadata=c)
        self.slm.put(self.slm.SENTINAL)


class TestProcessQueue(multiprocessing.Process):
    def __init__(self, q, shape):
        super().__init__()
        self.shape = shape
        self.q = q

    def run(self):
        for c in range(10000):
            a = np.zeros(shape=self.shape) + c
            self.q.put((a, c))
        self.q.put((None, None))


def run_queue(size):
    q = multiprocessing.Queue(maxsize=1024)
    TestProcessQueue(q, (size, size)).start()
    a = 0
    while True:
        sample, meta = q.get()
        if sample is None:
            break
        a += sample[0, 0]
        assert sample[0, 0] == meta
    assert a == 49995000


def run_numpy_queue(size):
    slm = NumpyQueue((size, size), maxsize=1024)
    TestProcessNumpyQueue(slm).start()
    a = 0
    for sample, meta in slm:
        a += sample[0, 0]
        assert sample[0, 0] == meta
    assert a == 49995000


def run_numpy_queue2(size):
    """
    Alternate numpyqueue API
    """
    slm = NumpyQueue((size, size), maxsize=1024)
    TestProcessNumpyQueue(slm).start()
    a = 0
    while True:
        try:
            with slm.get(metadata=True) as (sample, meta):
                a += sample[0, 0]
                assert sample[0, 0] == meta
        except Empty:
            break
    assert a == 49995000


def run_experiment(fxn, size, N):
    import timeit
    stmt = "{}({})".format(fxn.__name__, size)
    return timeit.timeit(stmt=stmt, globals=globals(), number=N)


def test_numpy_queue():
    time_queue = run_experiment(run_queue, 128, 1)
    time_numpy1 = run_experiment(run_numpy_queue, 128, 1)
    time_numpy2 = run_experiment(run_numpy_queue2, 128, 1)
    assert time_queue > time_numpy1
    assert time_queue > time_numpy2
