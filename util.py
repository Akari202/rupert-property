from vec_utils_py import Vec3d, AngleRadians
import math

def ccw(p0: Vec3d, p1: Vec3d, p2: Vec3d) -> int:
    vec1 = Vec3d.new_from_to(p1, p0)
    vec2 = Vec3d.new_from_to(p1, p2)
    sign = vec1.cross(vec2).z
    if sign > 0:
        return 1
    elif sign == 0:
        return 0
    else:
        return -1

def convex_hull(points: list[Vec3d]) -> list[Vec3d]:
    p0 = min(points, key=lambda p: (p.y, p.x))
    def sort_key(p):
        vec = Vec3d.new_from_to(p0, p)
        return math.atan2(vec.y, vec.x)
    points.sort(key=sort_key, reverse=False)
    points.reverse()
    hull_stack = []
    for i in points:
        while len(hull_stack) > 1 and ccw(hull_stack[-2], hull_stack[-1], i) <= 0:
            hull_stack.pop()
        hull_stack.append(i)
    return hull_stack

def get_polygon_centroid_area(points: list[Vec3d]):
    points.append(points[0])
    x = [p.x for p in points]
    y = [p.y for p in points]
    area = 0
    centroid = Vec3d.zero()
    for i in range(len(points) - 1):
        step = x[i] * y[i + 1] - x[i + 1] * y[i]
        area += step
        centroid.x += (x[i] + x[i + 1]) * step
        centroid.y += (y[i] + y[i + 1]) * step
    area *= 0.5
    centroid.x /= 6.0 * area
    centroid.y /= 6.0 * area
    return (centroid, area)

