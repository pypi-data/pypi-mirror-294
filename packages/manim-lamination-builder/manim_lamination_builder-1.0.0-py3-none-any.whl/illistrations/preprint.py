from collections.abc import Iterable
from math import ceil
from typing import List, Optional
from manim import (
    BLUE,
    DOWN,
    GREEN,
    LEFT,
    PI,
    RIGHT,
    UP,
    Arrow,
    Circle,
    Group,
    MathTex,
    Tex,
    Text,
    config,
    np,
    tempconfig,
    Scene,
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
import ligth_theme
from manim_lamination_builder.custom_json import parse_lamination
from manim_lamination_builder.main import group
from manim_lamination_builder.points import FloatWrapper, LiftedAngle
from manim_lamination_builder.pull_back_tree import PullBackTree


class HorrifyingCase1(Scene):
    def construct(self):
        lam3 = parse_lamination(
            """{polygons:[[0.3, 0.5, 0.9]], points: [], degree:6}"""
        ).to_polygons()
        acolor = VisualSettings()
        acolor.point_color = BLUE
        As = [
            FloatWrapper(p.to_float(), 6, acolor)
            for p in lam3.polygons[0][2].siblings()
        ]
        Bs = lam3.polygons[0][0].siblings()
        lam3.points = As + list(Bs)
        labels = [
            "a_2",
            "b_2",
            "a_3",
            "\\alpha_1=b_3",
            "a_4",
            "b_4",
            "\\alpha_2",
            "a_5",
            "b_5",
            "a_6",
            "b_6",
            "\\alpha_3=a_1",
            "b_1",
        ]
        labels = [MathTex(lb) for lb in labels]
        lam3 = lam3.build(1.4, labels=labels)
        lam3.add(MathTex("P_1").shift(UP * 0.2, LEFT * 0.25))
        labels = ["\\beta_1", "\\beta_2", "\\beta_3"]
        labels = [MathTex(lb) for lb in labels]

        lam4 = parse_lamination(
            """{polygons:[[0.3, 0.6, 0.9]], points: [], degree:2}"""
        ).to_polygons()
        lam4 = lam4.build(1.4, labels=labels)
        lam4.add(MathTex("P_2").shift(DOWN * 0.1 + 0.1 * LEFT))
        lam4.add(MathTex("G'").shift(RIGHT * 0.6 + 0.5 * UP))
        after = Text("after:")
        bottom = Group(after, lam3, Arrow(), lam4).arrange().to_edge(DOWN)
        self.add(bottom)

        lam1 = GapLamination.empty(2).build(1.4)
        lam1.add(MathTex("R"))
        arr1 = Arrow()
        lam2 = GapLamination.empty(2).build(1.4)
        lam2.add(MathTex("G"))
        before = Text("before:")
        top = (
            Group(before, lam1, arr1, lam2).arrange().to_edge(UP).align_to(bottom, LEFT)
        )
        self.add(top)
        label2 = MathTex("n=6")
        label2.next_to(arr1, UP)
        self.add(label2)
        before.align_to(after, RIGHT)
        # top.next_to(before, RIGHT)


class HorrifyingCase2(Scene):
    def construct(self):
        lam3 = parse_lamination(
            """{polygons:[[0.3, 0.5, 0.9]], points: [], degree:6}"""
        ).to_polygons()
        original = lam3.polygons[0]
        acolor = VisualSettings()
        acolor.point_color = BLUE
        for a, b in [
            (original[0], original[1]),
            (original[1], original[2]),
            (original[2], original[0].lifted().centered(LiftedAngle(1, 2))),
        ]:

            def pred(p):
                x = p.lifted().centered(a.lifted())
                # if x == b or x == a:
                #     return False
                return a < x and x < b

            As = [
                FloatWrapper(p.to_float(), 6, acolor)
                for p in filter(pred, lam3.polygons[0][2].siblings())
            ]
            Bs = filter(pred, lam3.polygons[0][0].siblings())
            lam3.points += list(As)
            lam3.points += list(Bs)
        for i in range(3):
            original[i].visual_settings.point_color = GREEN
        lam3.points += original
        labels = [
            "a_{32}",
            "b_{32}",
            "a_{33}",
            "\\alpha_1",  # "a_{11}=\\alpha_1=b_{33}",
            "b_{11}",
            "a_{12}",
            "\\alpha_2",  # "a_{21}=\\alpha_2=b_{12}",
            "b_{21}",
            "a_{22}",
            "b_{22}",
            "a_{23}",
            "\\alpha_3",  # "a_{31}=\\alpha_3=b_{23}",
            "b_{31}",
        ]
        labels = [MathTex(lb) for lb in labels]
        lam3 = lam3.build(1.4, labels=labels)
        lam3.add(MathTex("P_1").shift(UP * 0.2, LEFT * 0.25))
        labels = ["\\beta_1", "\\beta_2", "\\beta_3"]
        labels = [MathTex(lb) for lb in labels]

        lam4 = parse_lamination(
            """{polygons:[[0.3, 0.6, 0.9]], points: [], degree:2}"""
        ).to_polygons()
        lam4 = lam4.build(1.4, labels=labels)
        lam4.add(MathTex("G'").shift(DOWN * 0.1 + 0.1 * LEFT))
        after = Text("after:")
        bottom = Group(after, lam3, Arrow(), lam4).arrange().to_edge(DOWN)
        self.add(bottom)

        lam1 = GapLamination.empty(2).build(1.4)
        lam1.add(MathTex("R"))
        arr1 = Arrow()
        lam2 = GapLamination.empty(2).build(1.4)
        lam2.add(MathTex("G"))
        before = Text("before:")
        top = (
            Group(before, lam1, arr1, lam2).arrange().to_edge(UP).align_to(bottom, LEFT)
        )
        self.add(top)
        label2 = MathTex("n=6")
        label2.next_to(arr1, UP)
        self.add(label2)
        before.align_to(after, RIGHT)
        # top.next_to(before, RIGHT)


class ConjugacyDiagram(Scene):
    def construct(self):
        bl = MathTex("B_\\infty")
        br = MathTex("B_\\infty")
        tl = MathTex("\\mathbb{C}/\\overline{\\mathbb{D}}")
        tr = MathTex("\\mathbb{C}/\\overline{\\mathbb{D}}")
        c = Arrow()
        self.add(Group(tl, c, tr).arrange())
        a = Arrow().rotate(PI * 1.5).next_to(tl, DOWN)
        b = Arrow().rotate(PI * 1.5).next_to(tr, DOWN)
        self.add(a, b)
        d = Arrow()
        self.add(Group(bl, d, br).arrange().next_to(Group(a, b), DOWN))
        self.add(MathTex("z^d").next_to(c, UP))
        self.add(MathTex("\\Psi").next_to(a, LEFT))
        self.add(MathTex("\\Psi").next_to(b, RIGHT))
        self.add(MathTex("p").next_to(d, DOWN))


start = parse_lamination("""{polygons:[['_100','_010','_001']],degree:2}""")
tree = PullBackTree.build(start, 5)

lams = list(filter(lambda lam: lam.trapped_criticality() == 0, tree.flatten()[-1]))
# print([lam.rational_lamination() for lam in lams])
config.preview = True
# tree.show_pullback_tree()


def reflect_across_y_equals_negative_x(point):
    # Extract x and y coordinates
    x, y = point[:2]

    # Calculate the reflected point
    reflected_x = -y
    reflected_y = -x

    # Create the new point, preserving the z-coordinate if it exists
    if len(point) == 3:
        return np.array([reflected_x, reflected_y, point[2]])
    else:
        return np.array([reflected_x, reflected_y, 0])


def permutation(i):
    if i == 2:
        return 3
    if i == 3:
        return 2
    return i


lams = tree.nx_generation_graph(5)[1]
print(lams[2].to_leafs().minor())  # shold be CCW of
print(lams[3].to_leafs().minor())

# tree.show_generation_graph(
#     5, 0.65 * 2, 2, False, reflect_across_y_equals_negative_x, permutation
# )
