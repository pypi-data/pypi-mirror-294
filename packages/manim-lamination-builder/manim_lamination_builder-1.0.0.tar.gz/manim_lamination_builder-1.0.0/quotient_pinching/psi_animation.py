from manim import *
from manim import tempconfig
from manim.mobject.vector_field import floor
from manim_lamination_builder import (
    AnimateLamination,
    GapLamination,
    rabbit_nth_pullback,
    sigma,
)
import numpy as np
import functools
from psi import apply_complex_function, f, f0, psi
import ligth_theme


def bottker_plane() -> VGroup:
    ret = VGroup()

    radius = 1.001
    # config.quality = "low_quality"
    while radius <= 3:
        circle = Circle(radius=radius, num_components=10000, stroke_width=2)
        ret.add(circle)
        radius *= radius

    for p in np.linspace(0, 1, 32):
        theta = np.pi * 2 * p
        line_end = 1.0001 * np.array([np.cos(theta), np.sin(theta), 0])
        line = Line(line_end, line_end * 3, tip_length=0, stroke_width=2)
        line.init_points()
        line.insert_n_curves(20)
        ret.add(line)
    ret.z_index = 1
    return ret


polar_to_cartesian = lambda pos: np.array(
    [pos[0] * np.cos(pos[1]), pos[0] * np.sin(pos[1]), 0]
)

img = ImageMobject("julia_set.png")
img.width = 4
img.height = 4
img.z_index = 0


class Posterstill1(Scene):
    def construct(self):
        # def bottker_plane() -> VGroup:
        #     ret = VGroup()
        #
        #     radius = 1.015
        #     while radius <= 3:
        #         circle = Circle(radius=radius, num_components=1000, stroke_width=2)
        #         ret.add(circle)
        #         radius *= radius
        #
        #     for p in np.linspace(0, 1, 16 + 1):
        #         theta = np.pi * 2 * p
        #         line_end = 1.0001 * np.array([np.cos(theta), np.sin(theta), 0])
        #         line = Line(line_end, line_end * 3, tip_length=0, stroke_width=2)
        #         line.init_points()
        #         line.insert_n_curves(10)
        #         ret.add(line)
        #     ret.z_index = 1
        #     return ret

        plane = bottker_plane()
        circ = Circle(color=BLACK, fill_opacity=1, radius=1)
        self.add(circ, plane)


class Posterstill2(Scene):
    def construct(self):
        # def bottker_plane() -> VGroup:
        #     ret = VGroup()
        #
        #     radius = 1.001
        #     while radius <= 3:
        #         circle = Circle(radius=radius, num_components=1000, stroke_width=2)
        #         ret.add(circle)
        #         radius *= radius
        #
        #     for p in np.linspace(0, 1, 16 + 1):
        #         theta = np.pi * 2 * p
        #         line_end = 1.0001 * np.array([np.cos(theta), np.sin(theta), 0])
        #         line = Line(line_end, line_end * 3, tip_length=0, stroke_width=2)
        #         line.init_points()
        #         line.insert_n_curves(10)
        #         ret.add(line)
        #     ret.z_index = 1
        #     return ret

        plane = bottker_plane()
        zplane = apply_complex_function(plane, psi)
        self.add(img)
        self.add(zplane)


A = 1.1625 * 2 * 1.15
B = 1.575 * 2 * 1.15
pix = 400
with tempconfig(
    {
        # "preview": True,
        "pixel_height": floor(A * pix),
        "pixel_width": floor(B * pix),
        "frame_height": A,
        "frame_width": B,
        "disable_caching": True,
        # "top": (top + buf) * UP,
        # "left_size": left - buf,
    }
):
    Posterstill1().render()
    # Posterstill2().render()
