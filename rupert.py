from util import convex_hull, get_polygon_centroid_area
from cube import Cube
from vec_utils_py import Quat
import matplotlib.pyplot as plt
from random import random

cube1 = Cube(1)
cube1.align()
cube2 = Cube(1)
quat = Quat(random(), random(), random(), random())
magnitude = quat.magnitude()
quat = Quat(quat.w / magnitude, quat.i / magnitude, quat.j / magnitude, quat.k / magnitude)
cube2.rotate(quat)
print(get_polygon_centroid_area(convex_hull(cube2.project())))



# fig = plt.figure()
# ax = fig.add_subplot(projection="3d")
# cube1.plot(ax, "base")
# cube2.plot(ax, "rotated")
# ax.legend()
# ax.set_aspect("equal")
# plt.show()

fig = plt.figure()
ax = fig.add_subplot()
cube1.plot_hull(ax, "base")
# cube2.plot_hull(ax, "rotated")
cube2.align()
cube2.plot_hull(ax, "rotated aligned")
# ax.legend()
ax.grid()
ax.set_aspect("equal")
plt.show()
