from copy import deepcopy
from math import ceil
from typing import Tuple

from manim import (
    BLACK,
    DOWN,
    LEFT,
    RIGHT,
    UP,
    WHITE,
    Annulus,
    Arrow,
    Circle,
    Group,
    MathTex,
    Scene,
    Text,
    config,
    tempconfig,
)
from manim.utils.file_ops import config
from manim_lamination_builder import (
    CriticalTree,
    FloatWrapper,
    GapLamination,
    VisualSettings,
    custom_dump,
    custom_parse,
    generate_unicritical_lamination,
    next_pull_back,
    remove_non_original_pollygons,
    double_orbit,
    add_points_preimages,
    rabbit_nth_pullback,
)
from manim_lamination_builder import generate
from manim_lamination_builder.generate import Colors, unicritical_polygon
from manim_lamination_builder.morph import (
    remove_occluded,
    interpolate_quotent_of_region_of_rotational_polygon,
)
from manim_lamination_builder import construct_tree

config.background_color = WHITE
config.quality = "fourk_quality"
config.preview = False


class Unicritical3_3_Flat(Scene):
    def construct(self):
        start = GapLamination([unicritical_polygon(3, 3)], [], 3).to_leafs()
        laminations = list(map(lambda lam: lam.to_polygons(), next_pull_back(start)))
        for lam in laminations:
            lam = lam.auto_populate()
        laminations = [laminations[2], laminations[0], laminations[3], laminations[1]]
        group = Group(*[lamination.build() for lamination in laminations])
        group = group.arrange()
        group.scale(
            1
            / max(
                group.width / config.frame_width + 0.01,
                group.height / config.frame_height + 0.01,
            )
        )
        self.add(group)


# with tempconfig({"pixel_height": ceil(config.pixel_width / 4)}):
#     Unicritical3_3_Flat().render()


class FullRecursiveExplanaitionStill(Scene):
    def construct(self):
        lam = remove_non_original_pollygons(generate_unicritical_lamination(3, 3))[0]
        orlam = deepcopy(lam)
        A = deepcopy(orlam.points[0])
        A.visual_settings = VisualSettings(stroke_color=Colors.red)
        orlam.polygons.append([A, FloatWrapper(A.to_float() + 1 / 3)])
        original = orlam.build()
        setup = interpolate_quotent_of_region_of_rotational_polygon(lam).build()
        portraits = map(
            lambda l: interpolate_quotent_of_region_of_rotational_polygon(l).build(),
            generate_unicritical_lamination(3, 3),
        )
        arrow = MathTex(r"\to", color=BLACK, font_size=70)
        arrow2 = MathTex(r"\to", color=BLACK, font_size=70)

        stuff = Group(original, arrow, setup, arrow2, *portraits)
        stuff.arrange()
        self.add(stuff)


# A = 1700
# B = 10400
# with tempconfig(
#     {
#         "pixel_height": A,
#         "pixel_width": B,
#         "frame_height": A / 800,
#         "frame_width": B / 800,
#     }
# ):
#     FullRecursiveExplanaitionStill().render()

lam43 = remove_non_original_pollygons(generate_unicritical_lamination(4, 3))[0]
lam43 = interpolate_quotent_of_region_of_rotational_polygon(lam43)
lam43.points.insert(0, lam43.points.pop(8))

cowordinates = [
    (0, 0, 2),
    (1, 0, 1),
    (0, 1, 1),
    (2, 0, 0),
    (1, 1, 0),
    (0, 2, 0),
]


def interpret_cowordinate(t: Tuple[int, int, int], lam=lam43) -> GapLamination:
    i = 3
    ret = deepcopy(lam)
    ret.polygons.append([
        lam.points[0],
        FloatWrapper(lam.points[1].to_float() + 1 / i * t[0]),
        FloatWrapper(lam.points[2].to_float() + 1 / i * (t[0] + t[1])),
    ])
    return ret


mono_pollygons = [interpret_cowordinate(t) for t in cowordinates]


class RecursiveExplanaitionD(Scene):
    def construct(self):
        # from main.group
        group = Group(*[lamination.build() for lamination in mono_pollygons])
        for i in range(6):
            textmob = Text(str(cowordinates[i]), font_size=25)
            textmob.set_color(BLACK)
            textmob.move_to(DOWN * 1.4)
            group.submobjects[i].add(textmob)
        group = group.arrange_in_grid()
        group.scale(
            1
            / max(
                group.width / config.frame_width + 0.01,
                group.height / config.frame_height + 0.01,
            )
        )
        group.shift(UP * 0.25)
        self.add(group)


# A = 3300
# B = 4000
# with tempconfig(
#     {
#         "pixel_height": A,
#         "pixel_width": B,
#         "frame_height": A/400,
#         "frame_width": B/400,
#     }
# ):
#     RecursiveExplanaitionD().render()


class SingleTerm(Scene):
    def construct(self):
        lam = interpolate_quotent_of_region_of_rotational_polygon(
            remove_non_original_pollygons(generate_unicritical_lamination(5, 3))[0]
        )
        lam.points.insert(0, lam.points.pop())
        lam.polygons.append([lam.points[0], lam.points[4], lam.points[5]])

        mob = lam.build(1.9).move_to(LEFT * 4.8)
        self.add(mob, lam.build(1.9).move_to(LEFT * 4.8))
        self.add(MathTex(r"\to", color=BLACK, font_size=70).move_to(LEFT * 2))
        self.remove(mob)

        a, b, c = deepcopy(lam), deepcopy(lam), deepcopy(lam)
        ap, bp, cp = deepcopy(lam), deepcopy(lam), deepcopy(lam)
        ap.occlusion = (lam.points[3], lam.points[0])
        bp.occlusion = (lam.points[5], lam.points[4])
        cp.occlusion = (lam.points[11], lam.points[5])

        def just_after(p):
            return FloatWrapper(p.to_float() + 0.001)

        a.occlusion = (lam.points[4], just_after(lam.points[0]))
        b.occlusion = (lam.points[5], just_after(lam.points[4]))
        c.occlusion = (lam.points[0], just_after(lam.points[5]))
        a = remove_occluded(a, a.occlusion)
        b = remove_occluded(b, b.occlusion)
        c = remove_occluded(c, c.occlusion)
        A, B, C = (
            a.build(1.9),
            b.build(1.9),
            c.build(1.9),
        )
        self.add(
            A.move_to(0.15 * LEFT),
            B.move_to(2 * RIGHT),
            C.move_to(4.8 * RIGHT),
        )


# with tempconfig({"pixel_height": ceil(config.pixel_width * 0.28)}):
#     SingleTerm().render()


class TreesPortrait(Scene):
    def construct(self):
        lams = list(
            map(
                interpolate_quotent_of_region_of_rotational_polygon,
                generate_unicritical_lamination(4, 3),
            )
        )

        group = Group(*[
            Group(
                lam.build(0.5),
                construct_tree(lam).scale_to_fit_width(0.6),
            ).arrange_in_grid()
            for lam in lams
        ])
        group = group.arrange_in_grid(rows=4)
        group.scale(
            1
            / max(
                group.width / config.frame_width + 0.01,
                group.height / config.frame_height + 0.01,
            )
        )
        self.add(group)


# A = 3100
# B = 4000
# with tempconfig(
#     {
#         "pixel_height": A,
#         "pixel_width": B,
#         "frame_height": A / 400,
#         "frame_width": B / 400,
#         "preview": True,
#     }
# ):
#     TreesPortrait().render()


class NastyRotational(Scene):
    def construct(self):
        arrow = MathTex(r"\to", color=BLACK, font_size=70)
        B = remove_occluded(
            deepcopy(double_orbit),
            (double_orbit.points[5], double_orbit.points[0]),
        )
        group = Group(
            double_orbit.build(),
            arrow,
            remove_occluded(
                deepcopy(double_orbit), (double_orbit.points[1], double_orbit.points[0])
            ).build(),
            remove_occluded(
                deepcopy(double_orbit),
                (double_orbit.points[0].cleared(), double_orbit.points[5].cleared()),
            ).build(),
        )
        group.arrange()
        self.add(group)


# A = 2600
# B = 7800
# with tempconfig(
#     {
#         "pixel_height": A,
#         "pixel_width": B,
#         "frame_width": A/400,
#         "frame_height": B/400
#     }
# ):
#     NastyRotational().render()


class Invariant(Scene):
    def construct(self):
        rabbit_seed = GapLamination([unicritical_polygon(2, 3)], [], 2)
        for p in rabbit_seed.polygons[0]:
            p.visual_settings = VisualSettings(
                stroke_color=Colors.pure_red,
                stroke_width=0,
                polygon_color=Colors.pure_red,
            )
        rabbit_cord = CriticalTree.default()
        self.add(rabbit_cord.pull_back_n(rabbit_seed, 17).build())
        self.remove(self.mobjects[0].submobjects[0])
        self.add(
            Annulus(inner_radius=1.0, outer_radius=1.005, color=BLACK, stroke_width=0.0)
        )
        # self.add(Arrow(start=DOWN * 0.66, end=UP * 0.66, color=BLACK))


with tempconfig({
    "pixel_height": 16000,
    "pixel_width": 16000,
    "frame_height": 2.05,
    "frame_width": 2.05,
}):
    Invariant().render()
