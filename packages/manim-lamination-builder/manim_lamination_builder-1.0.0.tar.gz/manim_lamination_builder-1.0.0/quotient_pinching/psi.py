from manim import *
import numpy as np
import cmath

import functools

c = -0.122561166876657 + 0.744861766619737j


def f(z):
    return z**2 + c


def f0(z):
    d = 2
    return z**d


def inversef(z, guess):
    ret = cmath.sqrt(z - c)
    if np.abs(ret - guess) < np.abs(-ret - guess):
        return ret
    else:
        return -ret


def psi(w):
    assert np.abs(w) > 1
    if np.abs(w) > 1e150:
        return w
    return inversef(psi(f0(w)), w)


# import time
# start = time.perf_counter_ns()
# ret = psi(1.025+1.2875j)
# end = time.perf_counter_ns()
# print(ret, end-start)
## old way gives  (0.831862910941456+1.1429005122387517j) 767689
## this way gives (0.831862910941456+1.1429005122387519j) 97113
if False:
    from multiprocessing import Pool

    def process_point(p,function):
        out = function(complex(p[0], p[1]))
        return out.real * RIGHT + out.imag * UP

    def apply_complex_function(mob: Mobject, function) -> Mobject:
        ret = mob.copy()

        with Pool() as pool:
            out_points = pool.map(functools.partial(process_point, function=function), mob.points)

        for i,p in enumerate(out_points):
            ret.points[i] = p
        
        for i, submob in enumerate(ret.submobjects):
            ret.submobjects[i] = apply_complex_function(submob, function)
        return ret
else:
    def apply_complex_function(mob: Mobject, function) -> Mobject:
        ret = mob.copy()
        for i, p in enumerate(mob.points):
            out = function(complex(p[0], p[1]))
            ret.points[i] = out.real * RIGHT + out.imag * UP

        for i, submob in enumerate(ret.submobjects):
            ret.submobjects[i] = apply_complex_function(submob, function)
        return ret
