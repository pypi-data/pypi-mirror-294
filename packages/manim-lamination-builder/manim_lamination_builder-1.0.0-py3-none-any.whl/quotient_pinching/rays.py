# copied from qmnplane.cpp by Wolf Jung (C) 2007-2023.
import math
import cmath
from typing import Tuple
from manim import RIGHT, UP

from manim_lamination_builder import FloatWrapper, UnitPoint


def newton_ray(angle, re_c, im_c, quality):
    logR = 14.0
    u = math.exp(0.5 * logR)
    x = u * math.cos(angle)
    y = u * math.sin(angle)
    points = []
    for n in range(1, 103):
        angle *= 2
        angle %= math.tau
        for j in range(1, quality + 1):
            x, y, status = ray_newton(
                n, re_c, im_c, x, y, math.exp(-j * 0.69315 / quality) * logR, angle
            )

            points.append((x, y))
            if status != 0:
                if len(points) > 20:
                    print("accepted")
                return points
    return points


def ray_newton(n, re_c, im_c, x, y, rlog, angle) -> Tuple[float, float, int]:
    d = 1.0 + x * x + y * y
    for k in range(1, 61):
        fx = math.cos(angle)
        fy = math.sin(angle)
        t0 = math.exp(rlog) * fx - 0.5 * math.exp(-rlog) * (re_c * fx + im_c * fy)
        t1 = math.exp(rlog) * fy + 0.5 * math.exp(-rlog) * (re_c * fy - im_c * fx)
        fx = x
        fy = y
        px = 1.0
        py = 0.0
        for l in range(1, n + 1):
            u = 2.0 * (fx * px - fy * py)
            py = 2.0 * (fx * py + fy * px)
            px = u
            px += 1
            u = fx * fx
            v = fy * fy
            fy = 2.0 * fx * fy + im_c
            fx = u - v + re_c
            u += v
            v = px * px + py * py
            if u + v > 1.0e100:
                return x, y, 1
        fx -= t0
        fy -= t1
        if v < 1.0e-50:
            return x, y, 2
        u = (fx * px + fy * py) / v
        v = (fx * py - fy * px) / v
        px = u * u + v * v
        if px > 9.0 * d:
            return x, y, -1
        x -= u
        y += v
        d = px
        if px < 1.0e-28 and k >= 5:
            break
    return x, y, 0


scale = 4
def landing_point_in_rabbit(angle: UnitPoint):
    x, y = newton_ray(angle.to_angle(), -0.13, 0.77, 5)[-1]
    return RIGHT * x * scale + UP * y * scale


# print(landing_point_in_rabbit(FloatWrapper(4/7)))
print(newton_ray(math.tau*1/7, -0.13, 0.77, 5)[-1])

