from matplotlib.axes import Axes
from vec_utils_py import Vec3d, Quat
import matplotlib.pyplot as plt
import vec_utils_py
import math
from functools import lru_cache
from util import convex_hull, get_polygon_centroid_area

class Cube:
    def __init__(self, size: int):
        self.size = size
        self.vertices = [
                Vec3d(0,    0,      0),
                Vec3d(size, 0,      0),
                Vec3d(size, size,   0),
                Vec3d(0,    size,   0),
                Vec3d(0,    0,      size),
                Vec3d(size, 0,      size),
                Vec3d(size, size,   size),
                Vec3d(0,    size,   size)
                ]

    def rotate(self, quat: Quat):
        self.vertices = [quat.rotate(i) for i in self.vertices]

    @lru_cache(maxsize=1)
    def project(self, new: bool=False) -> list[Vec3d]:
        projection = [Vec3d(i.x, i.y, 0) for i in self.vertices]
        seen = set()
        return [x for x in projection if not (x in seen or seen.add(x))]

    def hull(self) -> list[Vec3d]:
        return convex_hull(self.project())

    def align(self):
        top = max(self.vertices, key=lambda p: p.y).y
        right = max(self.vertices, key=lambda p: p.x).x
        bottom = min(self.vertices, key=lambda p: p.y).y
        left = min(self.vertices, key=lambda p: p.x).x
        center = Vec3d((right + left) / 2, (top + bottom) / 2, 0)
        print(center)
        self.move(center)
        self.project(new=True)

    def move(self, vec: Vec3d):
        self.vertices = [i - vec for i in self.vertices]

    def plot(self, ax: Axes, name: str):
        order = []
        order.extend(self.vertices[:4])
        order.append(self.vertices[0])
        order.extend(self.vertices[4:])
        order.extend(self.vertices[4:6])
        order.extend(self.vertices[1:3])
        order.extend(self.vertices[6:])
        order.append(self.vertices[3])
        x = [i.x for i in order]
        y = [i.y for i in order]
        z = [i.z for i in order]
        ax.plot(x, y, z, label=name, marker="o")

    def plot_projection(self, ax: Axes, name: str):
        projection = self.project()
        x = [i.x for i in projection]
        y = [i.y for i in projection]
        for i, (x_coord, y_coord) in enumerate(zip(x, y)):
            plt.annotate(str(i), (x_coord, y_coord), textcoords="offset points", xytext=(0, 10), ha='center')
        ax.scatter(x, y, label=name, marker="o")

    def plot_hull(self, ax: Axes, name: str):
        projection = self.project()
        hull = convex_hull(projection)
        hull.append(hull[0])
        x = [i.x for i in hull]
        y = [i.y for i in hull]
        ax.plot(x, y, label=name, marker="o")
        # top = max(self.vertices, key=lambda p: p.y).y
        # right = max(self.vertices, key=lambda p: p.x).x
        # bottom = min(self.vertices, key=lambda p: p.y).y
        # left = min(self.vertices, key=lambda p: p.x).x
        # center = Vec3d((right + left) / 2, (top + bottom) / 2, 0)
        # ax.plot(center.x, center.y, label=name, marker="o")
