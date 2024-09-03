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


frame_constraint = 1 / max(
    1 / config.frame_width + 0.01, 1 / config.frame_height + 0.01
)
raidius = frame_constraint / 2

shape = unicritical_polygon(2, 3)
start = GapLamination(polygons=[shape], points=[], degree=2).to_leafs()
tree = PullBackTree.build(start, 4)


class PreimageLamination4(Scene):
    def construct(self):
        lams = [
            L.lifted().apply_function(
                lambda p: p.centered(NaryFraction.from_string(2, "_001"))
            )
            for L in tree.flatten()[-1]
        ]

        mobs = [L.build(1.5) for L in lams]
        self.add(Group(*mobs).arrange())
        # for i in range(len(lams)):
        #     self.add(mobs[i])
        #     print(i)
        self.wait(2)
        self.play(
            *[
                AnimateLamination(
                    initial=lams[i].to_polygons(),
                    final=sigma(lams[i].to_polygons()),
                    start_mobject=mobs[i],
                )
                for i in range(len(lams))
            ],
            run_time=4,
        )
        self.wait(1)


class PreimageLaminationArrow(Scene):
    def construct(self):
        A = tree.flatten()[-1]
        B = tree.flatten()[-2][0]
        middle = Arrow().shift(RIGHT)
        self.add(middle)
        self.add(Group(*[L.build(1.5) for L in A]).arrange_in_grid().shift(3 * LEFT))
        self.add(B.build(1.5).shift(4 * RIGHT))


class SiblingPortraitsIntro1(Scene):
    def construct(self):
        lam = rabbit_nth_pullback(4 + 1)

        top_polygon = next(
            filter(
                lambda poly: any(
                    [v == NaryFraction.from_string(2, "0010_001") for v in poly]
                ),
                lam.polygons,
            )
        )
        bottom_polygon = next(
            filter(
                lambda poly: any(
                    [v == NaryFraction.from_string(2, "1010_001") for v in poly]
                ),
                lam.polygons,
            )
        )
        lam = rabbit_nth_pullback(3 + 1)
        lam.points = list(top_polygon) + list(bottom_polygon) + list(sigma(top_polygon))
        print(top_polygon)
        print(sigma(top_polygon))
        print(sigma(sigma(top_polygon)))
        self.add(lam.build(3))


lf = interpolate_quotent_of_region_of_rotational_polygon


class SiblingPortraitsIntro2(Scene):
    def construct(self):
        shape = unicritical_polygon(3, 3)
        B = GapLamination(polygons=[shape], points=[], degree=3)
        A = next_pull_back(B.to_leafs())[0].to_polygons()
        middle = Arrow().shift(RIGHT)
        right = B.auto_populated().build(2.5)
        left = GapLamination(
            polygons=[], points=lf(A).to_polygons().auto_populated().points, degree=3
        ).build(2.5)
        self.add(Group(left, middle, right).arrange())


class SiblingPortraitsIntro3(Scene):
    def construct(self):
        shape = unicritical_polygon(3, 3)
        B = GapLamination(polygons=[shape], points=[], degree=3)
        A = next_pull_back(B.to_leafs())
        middle = Arrow().shift(RIGHT)
        self.add(middle)
        self.add(
            Group(*[lf(L.to_polygons().auto_populated()).build(1.5) for L in A])
            .arrange_in_grid()
            .shift(3 * LEFT)
        )
        self.add(B.auto_populated().build(1.5).shift(4 * RIGHT))


with tempconfig({
    "preview": True,
    "disable_caching": True,
}):
    SiblingPortraitsIntro2().render()
