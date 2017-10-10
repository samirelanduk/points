points
======

points is a Python library for performing linear algebra and geometry
calculations.

Example
-------

  >>> import points
  >>> vector = points.Vector(4, 3, 12)
  >>> vector.magnitude()
  >>> 13.0





Installing
----------

pip
~~~

points can be installed using pip:

``$ pip3 install points``

points is written for Python 3, and does not support Python 2.

If you get permission errors, try using ``sudo``:

``$ sudo pip3 install points``


Development
~~~~~~~~~~~

The repository for points, containing the most recent iteration, can be
found `here <http://github.com/samirelanduk/points/>`_. To clone the
points repository directly from there, use:

``$ git clone git://github.com/samirelanduk/points.git``


Requirements
~~~~~~~~~~~~

points has no dependencies, compiled or otherwise, and is pure Python.


Overview
--------

points is a library for performing geometry and linear algebra calculations.

Linear Algebra
~~~~~~~~~~~~~~

The ``Vector`` is the simplest linear algebra object. They can
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

You can get the component vectors like so:

  >>> vector.components()
  (<Vector [4, 0, 0]>, <Vector [0, 3, 0]>, <Vector [0, 0, 12]>)

You can add and remove values to the Vector in the same way you would with a
``list``:

  >>> vector.add(17)
  >>> vector.values()
  (4, 3, 12, 17)
  >>> vector.remove(17)
  >>> vector.values()
  (4, 3, 12)
  >>> vector.insert(1, 9)
  >>> vector.values()
  (4, 9, 3, 12)
  >>> vector.pop(1)
  9
  >>> vector.values()
  (4, 3, 12)

Vectors can be multiplied by scalar values (numbers) to get new Vectors:

  >>> vector * 5
  <Vector [20, 15, 60]>

Vectors can also be combined with other Vectors, with basic arithmetic, and also
with the dot product and angle between them:

  >>> vector2 = points.Vector(9, -1, 4)
  >>> vector + vector2
  <Vector [13, 2, 16]>
  >>> vector - vector2
  <Vector [-5, 4, 8]>
  >>> vector.distance_to(vector2)
  10.246950765959598
  >>> vector.dot(vector2)
  81
  >>> vector.cross(vector2)
  <Vector [24, 92, -31]>
  >>> vector.angle_with(vector2)
  0.8900119515744306
  >>> vector.angle_with(vector2, degrees=True)
  50.99392854141668


Changelog
---------

Release 0.2.0
~~~~~~~~~~~~~

`10 October 2017`

* Added Vector distances.
* Added component Vector generation.
* Added Vector cross product.


Release 0.1.0
~~~~~~~~~~~~~

`9 September 2017`

* Added basic Vector class.
* Added basic degrees/radians conversion decorator.
