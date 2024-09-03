"""
This approach cheats in the sense that it looks at the actual Julia set.
"""

import functools
from math import atan2, tan
from typing import Optional, List
from manim import (
    BLUE,
    ORIGIN,
    RIGHT,
    TAU,
    UP,
    WHITE,
    Arc,
    Line,
    Scene,
    Transform,
    np,
    rate_functions,
    CubicBezier,
)
from manim.animation.animation import config
from manim.mobject.geometry.arc import itertools
from manim_lamination_builder import (
    Chord,
    FloatWrapper,
    # Lamination,
    # UnitPoint,
    parse_lamination,
    rabbit_nth_pullback,
)
from numpy import repeat
from psi import psi
import cmath
from manim_lamination_builder import custom_dump


def get_convexity(in_list: List[UnitPoint]) -> Optional[List[FloatWrapper]]:
    """
    Retruns a sorted list of vetesies in CCW order such that the first is the boundary
    of the convex region. Wraping is handeld correctly and all points are taken from the same sheet
    of the reamon serface.
    If the Polygon is not convex in some way, return None.
    """
    sorted_list = sorted([p.cleared().to_float() for p in in_list])

    for i, p in enumerate(sorted_list):
        next_p = sorted_list[(i + 1) % len(in_list)]
        distance_ccw = (next_p - p) % 1
        if distance_ccw > 0.5:
            sorted_list = sorted([1 + p2 if p2 < next_p else p2 for p2 in sorted_list])
            return list(map(lambda p: FloatWrapper(p), sorted_list))

    return None


class CheatingPinch(Scene):
    def __init__(self, lamination: Lamination):
        def change_color(p):
            p.visual_settings.stroke_width = 2
            return p

        self.lamination = lamination.apply_function(change_color)
        self.all_vertecies_sorted = sorted(
            itertools.chain.from_iterable(self.lamination.polygons),
            key=lambda p: p.cleared().to_float(),
        )
        #  corresponds to its first ccw edge in the sorted or convex list
        self.initial_curves = []
        self.destination_curves = []
        self.polygons_handled = repeat(False, len(lamination.polygons))
        super().__init__()

    def add_initial_curve(self, p: UnitPoint, next_p: UnitPoint):
        bigness = (next_p.to_float() - p.to_float()) % 1
        arc = Arc(
            start_angle=p.to_angle(),
            angle=bigness * TAU,
            stroke_width=2,
        )
        self.initial_curves.append(arc)

    def point_positioning_function(self, polygon: List[UnitPoint]):
        points = []
        for angle in polygon:
            z = psi(1.000000001 * cmath.exp(angle.to_angle() * 1j))
            points.append(RIGHT * np.real(z) + UP * np.imag(z))
        return sum(points) / len(points)

    def angle_of_last_fatu_gap(self, polygon):
        """rotations"""
        first_ray = get_convexity(polygon)[0]
        z1 = psi(1.000000001 * cmath.exp(first_ray.to_angle() * 1j))
        z2 = psi(1.000005 * cmath.exp(first_ray.to_angle() * 1j))
        diff = z2 - z1
        angle_of_first_ray = np.angle(diff) / 2 / np.pi
        return angle_of_first_ray - 0.5 / len(polygon)

    def recursive_polygon_formation(self, polygon):
        cut_point_position = self.point_positioning_function(polygon)
        self.polygons_handled[self.lamination.polygons.index(polygon)] = True
        polygon_sorted = get_convexity(polygon)
        assert not polygon_sorted == None
        angle_of_final_fatue_gap = self.angle_of_last_fatu_gap(polygon)

        for i, p in enumerate(polygon_sorted):
            # test if recursion is needed
            angle_of_this_fatue_gap = angle_of_final_fatue_gap + (i + 1) / len(
                polygon_sorted
            )

            broad_index = self.all_vertecies_sorted.index(p.cleared())
            next_p = self.all_vertecies_sorted[
                (broad_index + 1) % len(self.all_vertecies_sorted)
            ]
            bigness = (next_p.to_float() - p.to_float()) % 1

            self.add_initial_curve(p, next_p)

            a = angle_of_this_fatue_gap + (-0.33) / len(polygon_sorted)
            A = FloatWrapper(a).to_cartesian() * bigness * 3
            if next_p in polygon:
                # repeated code
                b = a + 1 / len(polygon_sorted) * 0.66
                B = FloatWrapper(b).to_cartesian() * bigness * 3

                self.destination_curves += CubicBezier(
                    cut_point_position,
                    cut_point_position + A,
                    cut_point_position + B,
                    cut_point_position,
                    stroke_width=2,
                )
            else:
                adjacent_polygon = next(
                    filter(lambda poly: next_p in poly, self.lamination.polygons)
                )
                angle_of_this_cut_point_from_other = self.angle_of_last_fatu_gap(
                    adjacent_polygon
                ) + list(
                    map(lambda p: p.cleared(), get_convexity(adjacent_polygon))
                ).index(next_p) / len(adjacent_polygon)

                b = angle_of_this_cut_point_from_other + (0.33) / len(polygon_sorted)
                B = FloatWrapper(b).to_cartesian() * bigness * 3

                # destination curve
                other_cut_point_position = self.point_positioning_function(
                    adjacent_polygon
                )
                # scailar = 8 * Line(cut_point_position,other_cut_point_position).get_length()
                scailar = 3
                self.destination_curves += CubicBezier(
                    cut_point_position,
                    cut_point_position + A * scailar,
                    other_cut_point_position + B * scailar,
                    other_cut_point_position,
                    stroke_width=2,
                )

                if not self.polygons_handled[
                    self.lamination.polygons.index(adjacent_polygon)
                ]:
                    self.recursive_polygon_formation(adjacent_polygon)

    def construct(self):
        polygon_mobs = []
        polygon_destinations = []
        for i, polygon in enumerate(self.lamination.polygons):
            polygon_mobs += self.lamination.build().submobjects[1 + i]

            cut_point_position = self.point_positioning_function(polygon)
            polygon_destinations += CubicBezier(
                cut_point_position,
                cut_point_position,
                cut_point_position,
                cut_point_position,
                stroke_color=WHITE,
                stroke_width=2,
                color=BLUE,
            )

        # start procedure
        self.recursive_polygon_formation(self.lamination.polygons[0])

        self.add(*polygon_mobs)
        self.add(*self.initial_curves)
        self.wait(0.2)
        self.play(
            *[
                Transform(a, b)
                for a, b in zip(self.initial_curves, self.destination_curves)
            ],
            *[Transform(a, b) for a, b in zip(polygon_mobs, polygon_destinations)],
            run_time=1,
            rate_func=rate_functions.linear,
        )
        self.wait(0.2)


if __name__ == "__main__":
    # config.background_color = WHITE
    config.frame_width /= 3.5
    config.frame_height /= 3.5
    # config.preview = True
    lamination = rabbit_nth_pullback(6)
    CheatingPinch(lamination).render()
