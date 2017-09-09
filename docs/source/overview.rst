Overview
--------

points is a library for performing geometry and linear algebra calculations.

Linear Algebra
~~~~~~~~~~~~~~

The :py:class:`.Vector` is the simplest linear algebra object. They can
represent a point in space, or the attributes of an object.

  >>> import points
  >>> vector = points.Vector(4, 3, 12)
  >>> vector.values()
  (4, 3, 12)
  >>> vector[2]
  12
  >>> vector.length()
  3

Not that 'length' here refers to the number of values in the Vector - to get the
size of the line the Vector represents in space, you need the magnitude:

  >>> vector.magnitude()
  13.0

You can add and remove values to the Vector in the same way you would with a
``list``:

  >>> vector.add(17)
  >>> vector.values()
  (4, 3, 12, 17)
  vector.remove(17)
  >>> vector.values()
  (4, 3, 12)
  >>> vector.insert(1, 9)
  >>> vector.values()
  (4, 9, 3, 12)
  vector.pop(1)
  9
  >>> vector.values()
  (4, 3, 12)

Vectors can be multiplied by scalar values (numbers) to get new Vectors:

  >>> vector * 5
  <Vector [20, 15, 60]>

Vectors can also be combined with other Vectors:

  >>> vector2 = points.Vector(9, -1, 4)
  >>> vector + vector2
  <Vector [13, 2, 16]>
  >>> vector - vector2
  <Vector [-5, 4, 8]>
  >>> vector.dot(vector2)
  81
  >>> vector.angle_with(vector2)
  0.8900119515744306
  >>> vector.angle_with(vector2, degrees=True)
  50.99392854141668
