"""Contains functions for using trigonometry equations."""

import math
from .vectors import Vector

def translate_vectors(translation, *vectors):
    """Translates some vectors in space. The vectors will be changed in place.

    :raises TypeError: if non-vectors are given.
    :raises ValueError: if the vectors given don't match the dimension of the\
    translation.
    :param tuple translation: The translation values.
    :param \*vectors: The vectors to translate."""

    for v in vectors:
        if not isinstance(v, Vector):
            raise TypeError("Cannot translate {} - not a vector".format(v))
        if len(v._values) != len(translation):
            raise ValueError("Cannot translate {} - wrong dimension".format(v))
    for vector in vectors:
        vector._values = [val + d for val, d in zip(vector._values, translation)]



'''def degree_angle(func):
    """A decorator which takes a function that returns an angle in radians and
    confers upon it the ability to return it in degrees."""

    def new_func(*args, degrees=False, **kwargs):
        angle = func(*args, **kwargs)
        if degrees:
            return math.degrees(angle)
        return angle
    new_func.__name__ = func.__name__
    new_func.__doc__ = func.__doc__
    return new_func'''
