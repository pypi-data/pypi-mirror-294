from collections.abc import Iterable
from math import ceil
from typing import List, Optional
from manim import Arrow, Group, tempconfig, Scene
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


def convex_hull(vertices: Iterable[Angle]) -> Polygon:
    p = list(vertices)
    p.sort(key=lambda vertex: vertex.to_float() % 1)
    return tuple(p)


def full_all_bijection(original_full: GapLamination, eliminated_color) -> GapLamination:
    vertices = original_full.auto_populated().points
    vertices.sort(key=lambda vertex: vertex.to_float())
    eliminated_verticies = list(
        filter(lambda v: v.visual_settings.point_color == eliminated_color, vertices)
    )

    def find_polygon(vertex) -> Polygon:
        return next(filter(lambda poly: vertex in poly, original_full.polygons))

    def polygon_after(vertex) -> Polygon:
        nv = vertices[(vertices.index(vertex) + 1) % len(vertices)]
        return find_polygon(nv)

    def find_vertex(poly: Iterable[Angle]) -> Optional[Angle]:
        return next(
            filter(lambda v: v.visual_settings.point_color == eliminated_color, poly),
            None,
        )

    final_polygons: List[Polygon] = []
    while len(eliminated_verticies) != 0:
        eliminated = eliminated_verticies.pop()
        poly = set(find_polygon(eliminated))
        while eliminated is not None:
            poly = poly.union(polygon_after(eliminated))
            eliminated = find_vertex(poly)
            poly = set(
                filter(
                    lambda v: v.visual_settings.point_color != eliminated_color, poly
                )
            )
            if eliminated in eliminated_verticies:
                eliminated_verticies.remove(eliminated)
            else:
                eliminated = None
        final_polygons.append(convex_hull(poly))
    assert len(final_polygons) != 0
    return GapLamination(
        polygons=final_polygons, points=[], degree=original_full.degree
    ).auto_populated()


# def test_bijection():
#     lam = custom_parse("""
# {"points": ["0_010", "0_100", "1_001", "2_010", "2_100", "3_001", "1_010", "1_100", "2_
# 001", "0_001", "3_010", "3_100"], "degree": 4, "dark_theme": true, "polygons": [["0_010
# ", "0_100", "1_001"], ["2_010", "2_100", "3_001"], ["1_010", "1_100", "2_001"], ["0_001
# ", "3_010", "3_100"]]}
#                        """)
#     lam = full_all_bijection(lam, eliminated_color=get_color(0))
#     assert len(lam.polygons) == 1

# test_bijection()


d = 4
n = 2
pix = 200
index = 7


# shape = unicritical_polygon(d, n)
# lamination = GapLamination(polygons=[shape], points=[], degree=d)
# all_portraits = next_pull_back(lamination.to_leafs())


shape = unicritical_polygon(d, n + 1)
print(shape[0].visual_settings.point_size)
for p in shape:
    p.visual_settings.point_size *= 3
lamination = GapLamination(polygons=[shape], points=[], degree=d)
options = next_pull_back(lamination.to_leafs())
lf = interpolate_quotent_of_region_of_rotational_polygon
full_portraits = list(
    map(
        lambda L: lf(L.to_polygons()).auto_populated(),
        filter(
            pollygons_are_one_to_one,
            options,
        ),
    )
)

print(options[0].to_polygons().polygons[0][0].visual_settings.point_size)
# print(len(full_portraits))
# print(custom_dump(full_portraits[index]))
# with tempconfig({
#     "preview": True,
# }):
#     # Main([lamination.auto_populated()]).render()
#     # Main(full_portraits).render()
#     Main(
#         [full_portraits[index], full_all_bijection(full_portraits[index], get_color(0))]
#     ).render()
# exit()

all_portraits = list(
    map(
        lambda L: full_all_bijection(L, get_color(0)),
        full_portraits,
    )
)

group = Group(
    *[
        Group(
            pair[0].to_polygons().auto_populated().build(),
            Arrow(stroke_width=10).scale(0.6),
            pair[1].to_polygons().auto_populated().build(),
        ).arrange()
        for pair in zip(full_portraits, all_portraits)
    ]
)
group = group.arrange_in_grid(rows=4)


class FullAllBijection(Scene):
    def construct(self):
        self.add(group)


A = ceil(group.height)
B = ceil(group.width)
with tempconfig(
    {
        "pixel_height": A * pix,
        "pixel_width": B * pix,
        "frame_height": A,
        "frame_width": B,
        "preview": True,
    }
):
    FullAllBijection().render()
