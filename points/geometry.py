"""Contains functions for using trigonometry equations."""

from math import cos, sin, radians
from .vectors import Vector
from .matrices import Matrix

def round_vectors(func):
    """This decorator takes a function which handles vectors, and makes it round
    its values once complete."""

    def new(*args, trim=None, **kwargs):
        result = func(*args, **kwargs)
        if trim:
            for arg in args:
                if isinstance(arg, Vector):
                    arg._values = [round(val, trim) for val in arg._values]
        return result
    new.__doc__, new.__name__ = func.__doc__, func.__name__
    return new


def allow_degrees(func):
    """This decorator takes a function which takes an angle, and makes it able
    to take it in degrees as well as in radians."""

    def new(*args, degrees=False, **kwargs):
        if degrees: args = [radians(args[0])] + list(args[1:])
        return func(*args, **kwargs)
    new.__doc__, new.__name__ = func.__doc__, func.__name__
    return new


def translate_vectors(translation, *vectors):
    """Translates some vectors in space. The vectors will be changed in place.

    :param tuple translation: The translation values.
    :param \*vectors: The vectors to translate.
    :raises TypeError: if non-vectors are given.
    :raises ValueError: if the vectors given don't match the dimension of the\
    translation."""

    for v in vectors:
        if not isinstance(v, Vector):
            raise TypeError("Cannot translate {} - not a vector".format(v))
        if len(v._values) != len(translation):
            raise ValueError("Cannot translate {} - wrong dimension".format(v))
    for vector in vectors:
        vector._values = [val + d for val, d in zip(vector._values, translation)]


@round_vectors
@allow_degrees
def rotate_2d_vectors(angle, *vectors):
    """Rotates 2 dimensional vectors.

    :param float angle: The angle in radians.
    :param int trim: if given, the vector values will be rounded to this number\
    of decimal places at the end.
    :param bool degrees: if `True``, the angle given will be interpreted as\
    being in degrees, not radians.
    :param \*vectors: The vectors to rotate.
    :raises TypeError: if non-vectors are given.
    :raises ValueError: if the vectors given don't match the dimension of the\
    translation."""

    for v in vectors:
        if not isinstance(v, Vector):
            raise TypeError("Cannot rotate {} - not a vector".format(v))
        if len(v._values) != 2:
            raise ValueError("Cannot rotate {} - not 2D".format(v))
    matrix = Matrix([cos(angle), -sin(angle)], [sin(angle), cos(angle)])
    for vector in vectors:
        vector._values = (matrix @ vector)._values



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
