from manim_lamination_builder import (
    PullBackTree,
    parse_lamination,
    custom_dump,
    CriticalTree,
    Chord,
)
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
    FDL,
)


start = parse_lamination("""{polygons:[['_100','_010','_001']],degree:2}""").to_leafs()
start.leafs.update(
    parse_lamination("""{leafs:[['0_010','1_010']],degree:2}""").to_leafs().leafs
)
schem = CriticalTree.default()


class AproachingUnclean(Scene):
    def construct(self):
        original_polygon = (
            parse_lamination("""{polygons:[['_100','_010','_001']],degree:2}""")
            .to_polygons()
            .polygons[0]
        )
        print(original_polygon)
        # self.add(GapLamination([first_pull_back], [], 2).build(2))

        for i in range(1, 5):
            image_of_critical = (
                NaryFraction.from_string(2, "010" * (i - 1) + "001" + "_100"),
                NaryFraction.from_string(2, "010" * (i - 1) + "001" + "_010"),
                NaryFraction.from_string(2, "010" * (i - 1) + "010" + "_001"),
            )
            critical_polygon = []
            for d in ["0", "1"]:
                for p in image_of_critical:
                    critical_polygon.append(
                        NaryFraction.from_string(2, d + p.to_string())
                    )
            critical_polygon = Polygon(critical_polygon)
            n = critical_polygon[0].pre_period()

            critical_scheme = CriticalTree(
                first_ccw_end_point=critical_polygon[0], first_end_point_on_inside=True
            )

            initial_data = GapLamination([original_polygon], [], 2)
            lam = critical_scheme.pull_back_n(
                lam=initial_data, n=n
            ).to_polygons()
            lam.filtered(lambda a: a not in critical_polygon)
            lam.polygons.append(critical_polygon)
            lam = GapLamination(lam.polygons, [], 2)  # fixes polygon
            fdl = FDL(lam=lam, n=n).pulled_back_n(critical_scheme, i)
            lam = fdl.lam

            self.clear()
            self.add(lam.build(3.2))
            self.wait(1)

schem = CriticalTree()


class AproachingUnclean(Scene):
    def construct(self):
        original_polygon = (
            parse_lamination("""{polygons:[['_100','_010','_001']],degree:2}""")
            .to_polygons()
            .polygons[0]
        )
        print(original_polygon)
        # self.add(GapLamination([first_pull_back], [], 2).build(2))

        for i in range(1, 5):
            image_of_critical = (
                NaryFraction.from_string(2, "010" * (i - 1) + "001" + "_100"),
                NaryFraction.from_string(2, "010" * (i - 1) + "001" + "_010"),
                NaryFraction.from_string(2, "010" * (i - 1) + "010" + "_001"),
            )
            critical_polygon = []
            for d in ["0", "1"]:
                for p in image_of_critical:
                    critical_polygon.append(
                        NaryFraction.from_string(2, d + p.to_string())
                    )
            critical_polygon = Polygon(critical_polygon)
            n = critical_polygon[0].pre_period()

            critical_scheme = CriticalTree(
                first_ccw_end_point=critical_polygon[0], first_end_point_on_inside=True
            )

            initial_data = GapLamination([original_polygon], [], 2)
            lam = critical_scheme.pull_back_n(
                lam=initial_data, n=n
            ).to_polygons()
            lam.filtered(lambda a: a not in critical_polygon)
            lam.polygons.append(critical_polygon)
            lam = GapLamination(lam.polygons, [], 2)  # fixes polygon
            fdl = FDL(lam=lam, n=n).pulled_back_n(critical_scheme, i)
            lam = fdl.lam

            self.clear()
            self.add(lam.build(3.2))
            self.wait(1)

with tempconfig(
    {
        "preview": True,
        "disable_caching": True,
        # , "background": WHITE
    }
):
    AproachingUnclean().render()
    # Main([schem.pull_back_n(start, 4)]).render()
