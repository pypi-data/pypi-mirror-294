from copy import deepcopy
from math import ceil, floor
from typing import List, Tuple
from manim.utils.color import Colors
from manim_lamination_builder.generate import unicritical_polygon

import networkx as nx
from manim import (
    DOWN,
    LEFT,
    RED,
    UP,
    Group,
    Line,
    Mobject,
    Scene,
    config,
    tempconfig,
)
from manim.camera.camera import reduce
from manim_lamination_builder import (
    AnimateLamination,
    FloatWrapper,
    GapLamination,
    UnitPoint,
    custom_dump,
    custom_parse,
    generate_unicritical_lamination,
    remove_non_original_pollygons,
    first_polygon,
    make_regions,
)
from manim_lamination_builder.morph import (
    MorphOcclusion,
    interpolate_quotent_of_region_of_rotational_polygon,
    remove_occluded,
    result,
)

# meat of recursive argument
frame_constraint = 1 / max(
    1 / config.frame_width + 0.01, 1 / config.frame_height + 0.01
)
raidius = frame_constraint / 2


class MapForwardRabit(Scene):
    def __init__(self):
        super().__init__()
        self.pause = 1.3
        self.length = 5
        self.degree = 2
        self.order = 3

    def construct(self):
        lam = remove_non_original_pollygons(
            generate_unicritical_lamination(self.degree, self.order)
        )[0]
        mob = lam.build(raidius)
        self.add(mob)
        self.wait(self.pause)
        self.play(
            AnimateLamination(
                lam,
                lam.apply_function(lambda x: x.after_sigma()),
                mob,
                run_time=self.length,
            )
        )
        self.wait(self.pause)


class MapForward33(MapForwardRabit):
    def __init__(self):
        super().__init__()
        self.degree = 3
        self.order = 3


class MorphOutStill(Scene):
    def construct(self):
        lam = remove_non_original_pollygons(generate_unicritical_lamination(4, 3))[0]
        occlusion = (
            lam.polygons[0][0],
            FloatWrapper(lam.polygons[0][0].to_float() + 1 / 4),
        )
        lam.polygons.append(list(occlusion))
        mob = lam.build(raidius)
        mob.submobjects[2].set_color(RED)
        self.add(mob)


class MorphOut(Scene):
    def construct(self):
        lam = remove_non_original_pollygons(generate_unicritical_lamination(4, 3))[0]
        occlusion = (
            lam.polygons[0][0],
            FloatWrapper(lam.polygons[0][0].to_float() + 1 / 4),
        )
        lam.polygons.append(list(occlusion))
        mob = lam.build(raidius)
        mob.submobjects[2].set_color(RED)
        self.add(mob)
        self.wait(1.3)
        self.remove(mob)
        lam.occlusion = occlusion
        print(custom_dump(occlusion))
        lam = remove_occluded(lam, occlusion)
        mob = lam.build(raidius)
        self.add(mob)
        self.wait(1.3)
        self.play(MorphOcclusion(lam, occlusion, mob, run_time=5))
        self.wait(3)


class TreeCreator(Scene):
    def get_values(self):
        return 1, interpolate_quotent_of_region_of_rotational_polygon(
            generate_unicritical_lamination(4, 3)[3]
        )

    def construct(self):
        radius, lam = self.get_values()
        vertical_position = 3 * UP
        buds = [(lam, lam.build(radius).move_to(vertical_position))]
        self.add(buds[0][1])
        self.add(lam.build(2).shift(5 * LEFT + 1.9 * UP))
        self.wait(1)

        def render_individual_polygon(poly: List[UnitPoint]) -> Mobject:
            return GapLamination([poly], [], lam.degree).build(radius).submobjects[-1]

        while len(buds) != 0:
            vertical_position += 2 * radius * DOWN
            new_buds = []
            items = []
            for lam, mob in buds:
                center = mob.submobjects[0].get_arc_center()
                self.remove(mob)
                polygon = render_individual_polygon(first_polygon(lam)).shift(center)
                self.add(polygon)
                regions = make_regions(lam)
                mobs = [reg.build(radius).shift(center) for reg in regions]
                self.add(*mobs)

                for i, reg in enumerate(regions):
                    if len(reg.polygons) != 0:
                        new_buds.append((reg, mobs[i]))
                    items.append((polygon, mobs, regions))

            self.wait(2)
            self.play(
                Group(
                    *reduce(
                        lambda x, y: x + y, [children for _, children, _ in items], []
                    )
                )
                .animate.arrange()
                .move_to(vertical_position)
            )
            for parent, children, regions in items:
                for child, region in zip(children, regions):
                    child_center = child.get_center()
                    if len(region.polygons) != 0:
                        child_center = (
                            child.submobjects[0].get_arc_center()
                            + render_individual_polygon(
                                first_polygon(region)
                            ).get_center()
                        )
                    self.add(
                        Line(parent.get_center(), child_center).set_stroke(
                            color=RED, opacity=0.3
                        )
                    )

            self.wait(3)

            buds = new_buds

        self.wait(3)


class TreeCreatorB(TreeCreator):
    def get_values(self):
        return 0.8, interpolate_quotent_of_region_of_rotational_polygon(
            generate_unicritical_lamination(6, 3)[20]
        )
