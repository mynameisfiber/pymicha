#!/usr/bin/env python

from pybloom_live import BloomFilter


class MultigramSearch(object):
    """
    This datastructure is useful when you have many potential subsequence that
    you wish to find within a target sequence. An example is finding which of
    several thousands of phrases occures within a given text.

    The algorithm is a standard Rabin-Karp string search algorithm [1] using
    bloom filters as the lookup for better space efficency.

    [1]: https://en.wikipedia.org/wiki/Rabin%E2%80%93Karp_algorithm

    >>> import multigram_search
    >>> mgs = multigram_search.MultigramSearch([("a", "b", "c"),
                                                ("o", "c", "z"),
                                                ("z", "y")])
    >>> list(mgs.intersection("hello world you a b c foo".split(" ")))
    [['a', 'b', 'c']]
    """
    def __init__(self, ngrams, delimiter='####', stop='^^^^',
                 error=0.0001, error_tightening_ratio=0.5):
        self.blooms = []
        self.error = error
        self.error_tightening_ratio = error_tightening_ratio
        self.min_ngram = min(len(d) for d in ngrams) or 1
        self.max_ngram = max(len(d) for d in ngrams)
        self.delimiter = delimiter
        self.STOP = stop
        self._build_structure(ngrams)

    def _build_structure(self, ngrams):
        delimiter = self.delimiter
        STOP = self.STOP
        for i, n in enumerate(range(self.min_ngram, self.max_ngram+1)):
            num_items = sum(1 for x in ngrams if len(x) >= n)
            # we tighten the error so that the compounded error converges to
            # the desired error
            cur_error = self.error * (self.error_tightening_ratio ** i)
            bloom = BloomFilter(num_items, error_rate=cur_error)
            for item in filter(None, ngrams):
                if len(item) >= n:
                    print("adding: ", item[:n])
                    bloom.add(delimiter.join(item[:n]))
                elif len(item) + 1 == n:
                    print("adding: ", item[:n], STOP)
                    bloom.add(delimiter.join(item) + STOP)
            self.blooms.append(bloom)

    def intersection(self, text):
        i = 0
        offset = self.min_ngram
        L = len(text) - offset
        delimiter = self.delimiter
        while i <= L:
            for N, bloom in enumerate(self.blooms):
                test = delimiter.join(text[i:i+N+offset])
                if test not in bloom:
                    if N > 0:
                        new_test = delimiter.join(text[i:i+N+offset-1])
                        if (new_test + self.STOP) in bloom:
                            yield text[i:i+N+offset-1]
                    break
                elif N == self.max_ngram - offset and test in bloom:
                    yield text[i:i+N+offset]
            i += N + 1
