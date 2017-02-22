from functools import total_ordering


@total_ordering
class SuperNone(object):
    """
    SuperNone is the most None an object can get. Anything that touches this
    object itself becomes a SuperNone and this object intrinsically does
    nothing.

    NOTE: By convention, this object will always be less than anything it is
    compared with
    """
    # general properties / methods
    def __getattr__(self, *args, **kwargs):
        return self

    def __call__(self, *args, **kwargs):
        return self

    def __setattr__(self, *args, **kwargs):
        pass

    # sequence methods
    def __contains__(self, *args, **kwargs):
        return None

    # ordering
    def __lt__(self, *args, **kwargs):
        return True

    def __eq__(self, *args, **kwargs):
        return False

    # math
    def __add__(self, *args, **kwargs):
        return self

    def __sub__(self, *args, **kwargs):
        return self

    def __mul__(self, *args, **kwargs):
        return self

    def __div__(self, *args, **kwargs):
        return self

    # representations
    def __repr__(self):
        return "<SuperNone>"
