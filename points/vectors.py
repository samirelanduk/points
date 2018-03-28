"""Contains the Vector class."""

from math import sqrt

class Vector:

    def __init__(self, *values):
        if len(values) == 1:
            try:
                self._values = list(values[0])
                return
            except: pass
        self._values = list(values)


    def __repr__(self):
        return "<Vector {}>".format(self._values)


    def __str__(self):
        if len(self._values) >= 10:
            values = self._values[:2] + [] + self._values[-2:]
            return "<Vector [{}, {}, (...{} items omitted...), {}, {}]>".format(
             self._values[0], self._values[1], len(self._values) - 4,
             self._values[-2], self._values[-1]
            )
        return repr(self)


    def __contains__(self, item):
        return item in self._values


    def __iter__(self):
        return iter(self._values)


    def __getitem__(self, index):
        return self._values[index]


    def __setitem__(self, index, value):
        self._values[index] = value


    def __len__(self):
        return len(self._values)


    def __add__(self, other):
        if not isinstance(other, Vector):
            raise TypeError("Cannot add {} - not a Vector".format(other))
        if len(self) != len(other):
            raise ValueError("Cannot add {} - unequal length".format(other))
        return Vector(v1 + v2 for v1, v2 in zip(self._values, other._values))


    def __sub__(self, other):
        if not isinstance(other, Vector):
            raise TypeError("Cannot subtract {} - not a Vector".format(other))
        if len(self) != len(other):
            raise ValueError("Cannot subtract {} - unequal length".format(other))
        return Vector(v1 - v2 for v1, v2 in zip(self._values, other._values))


    def __mul__(self, other):
        if isinstance(other, Vector):
            raise TypeError("'*' is reserved for scalar multiplication")
        else:
            return Vector([v * other for v in self._values])


    def __rmul__(self, other):
        return self * other


    def length(self):
        """Returns the length of the Vector. This is the number of values it
        contains, not its :py:meth:`magnitude`.

        :rtype: ``int``"""

        return len(self)


    def values(self):
        """Returns the values in the Vector.

        :rtype: ``tuple``"""

        return tuple(self._values)


    def magnitude(self):
        """Returns the magnitude of the Vector - the length of the line it
        represents in space.

        :rtype: ``float``"""

        return sqrt(sum([x**2 for x in self._values]))


    def append(self, value):
        """Adds a value to the end of the Vector.

        :param value: the value to add."""

        self._values.append(value)


    def insert(self, index, value):
        """Insertes a value into the Vector.

        :param int index: The location to insert to.
        :param value: the value to add."""

        self._values.insert(index, value)


    def remove(self, value):
        """Removes a value from the Vector.

        :param value: the value to remove."""

        self._values.remove(value)


    def pop(self, index=-1):
        """Removes a value from the Vector and returns it.

        :param index: the index to remove, default being ``-1``.
        :returns: the removed value."""

        return self._values.pop(index)


    def components(self):
        """Returns the individual components that sum to make up the Vector.

        :returns: ``tuple`` of ``Vector``"""

        components = []
        for index, value in enumerate(self._values):
            component_values = [0] * len(self._values)
            component_values[index] = value
            components.append(Vector(*component_values))
        return tuple(components)


    def linearly_dependent_on(self, *vectors):
        """Checks if this Vector is linearly independent of a set of other
        vectors - that is, whether it is impossible to construct this Vector
        from a linear combination of the other Vectors.

        :param \*vectors: The vectors to check against.
        :rtype: ``bool``"""

        return self in VectorSpan(*vectors)


    def linearly_independent_of(self, *vectors):
        """Checks if this Vector is linearly dependent on a set of other
        vectors - that is, whether it is possible to construct this Vector from
        a linear combination of the other Vectors.

        :param \*vectors: The vectors to check against.
        :rtype: ``bool``"""

        return not self.linearly_dependent_on(*vectors)


    def span(self):
        """Returns the Vector's span - the set of all Vectors that can be
        constructed by scaling this Vector.

        :rtype: ``VectorSpan``"""

        return VectorSpan(self)


    def span_with(self, *vectors):
        """Returns the span of this Vector and others - the set of all Vectors
        that can be constructed by scaling and adding the Vectors.

        :rtype: ``VectorSpan``"""

        return VectorSpan(self, *vectors)


    def dot(self, other):
        """Returns the dot product between this vector and another.

        :param Vector other: The other Vector.
        :raises TypeError: If a non-Vector is given.
        :raises ValueError: If the Vectors are of different lengths.
        :rtype: ``float``"""

        if not isinstance(other, Vector):
            raise TypeError("{} is not a Vector".format(other))
        if self.length() != other.length():
            raise ValueError("{} and {} not equal length".format(self, other))
        return sum([u_i * v_i for u_i, v_i in zip(self._values, other._values)])


    def cross(self, other):
        """Returns the cross product between this vector and another. Only
        three-dimensional Vectors can do this (Vectors of length 3).

        :param Vector other: The other Vector.
        :raises TypeError: if a non-Vector is given.
        :raises ValueError: if the Vectors are not three-dimensional.
        :rtype: ``Vector``"""

        if not isinstance(other, Vector):
            raise TypeError("{} is not a Vector".format(other))
        values, other = self._values, other._values
        if len(values) != 3 or len(other) != 3:
            raise ValueError("{} or {} is not 3D".format(self, other))
        return Vector(
         values[1] * other[2] - values[2] * other[1],
         values[2] * other[0] - values[0] * other[2],
         values[0] * other[1] - values[1] * other[0]
        )



class VectorSpan:
    """A VectorSpan represents all the vectors that can be obtained by
    performing linear combinations of some starter set of Vectors.

    A Vector is ``in`` this span if it can be constructed from a linear
    combination of the defining Vectors. This is calculated using Gaussian
    elimination.

    :param \*vectors: The Vectors which define the span. Any vectors that are\
    linearly dependent on the others will be discarded.
    :raises ValueError: if Vectors of different dimensions are provided."""

    def __init__(self, *vectors):
        self._vectors = {vectors[0]}
        self._dimension = len(vectors[0])
        for v in vectors[1:]:
            if len(v) != self._dimension: raise ValueError(
             "{} has Vectors of different dimensions".format(vectors)
            )
            if v.linearly_independent_of(*self._vectors):
                self._vectors.add(v)


    def __repr__(self):
        return "<VectorSpan{} - {} dimensions>".format(
         " of " + repr(
          list(list(self._vectors)[0].values())
         ) if len(self._vectors) == 1 else "", self._dimension
        )


    def __contains__(self, vector):
        if len(vector) != self._dimension: return False
        if set(vector.values()) == {0}: return True
        if len(self._vectors) == 1:
            one_vector = list(self._vectors)[0]
            if set(one_vector.values()) == {0}: return False
            if any(val1 == 0 and val2 != 0 for val1, val2
             in zip(vector.values(), one_vector.values())): return False
            if len(set([v1 / v2 for v1, v2 in zip(one_vector, vector)])) == 1:
                return True
        else:
            from .matrices import Matrix
            augmented = Matrix(*self._vectors, vector, columns=True)
            augmented.gauss()
            for row in augmented.rows():
                if set(row[:-1]) == {0} and row[-1] != 0: return False
            return True


    def dimension(self):
        """The Vector space that the Span inhabits - any vectors of a different
        Vector will never be ``in`` this Span.

        :rtype: ``int``"""

        return self._dimension


    def rank(self):
        """The dimensions of the space the VectorSpan spans - regardless of the
        overall Vector Space it inhabits.

        For example a Vector Span in three dimensional space might have a rank
        of 2 if it only spans a plane within that space.

        :rtype: ``int``"""

        return len(self._vectors)
'''

, sin, cos, acos, degrees
from .geometry import degree_angle

class Vector:
    """A vector is a sequence of numbers. They can represent a point in space,
    or the attributes of an object.

    Vectors can be added and subtracted with ``+`` and ``-``, but ``*`` is
    reserved for scalar multiplication - you can use it to multiply the vector
    by a number but not by another vector (there are special methods for this).

    :param values: The numbers that make up the Vector. If a single sequence is\
    given, that sequence will be unpacked to make the vector.
    :raises TypeError: if the values given are not numeric."""


    def rotate(self, angle, axis="x"):
        """A 2 dimensional vector can be rotated by supplying an angle in
        radians. A 3 dimensional vector can be rotated by supplying an angle in
        radians and an axis to rotate around (``"x"``, ``"y"`` or ``"z"``).

        All rotation is right handed. No vectors of other dimensions can
        currently be rotated.

        :param float angle: the angle to rotate by.
        :param str axis: the axis to rotate around if in 3D.
        :raises ValueError: if the vector length is not 2 or 3.
        :raises ValueError: if axis given is invalid."""

        from .matrices import Matrix
        matrix = None
        if len(self._values) == 2:
            matrix = Matrix([cos(angle), -sin(angle)], [sin(angle), cos(angle)])
        elif len(self._values) == 3:
            if axis == "x":
                matrix = Matrix(
                 [1, 0, 0],
                 [0, cos(angle), -sin(angle)],
                 [0, sin(angle), cos(angle)]
                )
            elif axis == "y":
                matrix = Matrix(
                 [cos(angle), 0, sin(angle)],
                 [0, 1, 0],
                 [-sin(angle), 0, cos(angle)]
                )
            elif axis == "z":
                matrix = Matrix(
                 [cos(angle), -sin(angle), 0],
                 [sin(angle), cos(angle), 0],
                 [0, 0, 1]
                )
            else:
                raise ValueError("Axis '{}' is not z, y or z".format(axis))
        else:
            raise ValueError("Only 2 and 3 dimensional vectors can rotate")
        self._values = (matrix @ self)._values



    def distance_to(self, other):
        """Returns the distance between this and another vector, when
        originating at the origin.

        :param Vector other: the other Vector.
        :rtype: ``float``"""

        vector = self - other
        return vector.magnitude()








    @degree_angle
    def angle_with(self, other):
        """Returns the angle between this vector and another, in radians.

        :param Vector other: The other Vector.
        :param bool degrees: If ``True`` the angle will be returned in degrees.
        :raises TypeError: If a non-Vector is given.
        :rtype: ``float``"""

        if not isinstance(other, Vector):
            raise TypeError("{} is not a Vector".format(other))
        if self.length() != other.length():
            raise ValueError("{} and {} not equal length".format(self, other))
        return acos(self.dot(other) / (self.magnitude() * other.magnitude()))
'''
