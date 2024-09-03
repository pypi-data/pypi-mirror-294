from manim import (
    DOWN,
    LEFT,
    RIGHT,
    Arrow,
    Group,
    Scene,
    tempconfig,
    BLACK,
    WHITE,
    config,
)
from manim_lamination_builder import (
    NaryFraction,
    PullBackTree,
    pull_backs,
    rabbit_nth_pullback,
    AnimateLamination,
    sigma,
    unicritical_polygon,
    GapLamination,
)
from manim_lamination_builder import (
    Angle,
    GapLamination,
    Main,
    Polygon,
    VisualSettings,
    custom_dump,
    custom_parse,
    unicritical_polygon,
    next_pull_back,
    interpolate_quotent_of_region_of_rotational_polygon,
    pollygons_are_one_to_one,
    construct_tree,
    get_color,
)
from manim_lamination_builder.custom_json import parse_lamination

frame_constraint = 1 / max(
    1 / config.frame_width + 0.01, 1 / config.frame_height + 0.01
)
raidius = frame_constraint / 2


class Show(Scene):
    def construct(self):
        lam = parse_lamination(
            """{degree:3,polygons:[["_011", "_101", "_110"], ["_211", "_121", "_112"]]}"""
        )

        self.add(lam.build(raidius))


with tempconfig(
    {
        "preview": True,
        "disable_caching": True,
    }
):
    Show().render()
