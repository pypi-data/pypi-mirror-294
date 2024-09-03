from manim import RED, Graph, Scene, config, tempconfig
from math import ceil
from manim_lamination_builder import (
    Chord,
    LeafLamination,
    TreeRender,
    PullBackTree,
    parse_lamination,
    custom_parse,
    rabbit_nth_pullback,
)
import networkx as nx

from manim_lamination_builder.lamination import GapLamination

config.preview = True

# start = LeafLamination(leafs=[Chord("_01", "_10")], points=[], degree=2)
start = parse_lamination(
    """{degree:3, polygons:[["_001","_010","_100"],["_112","_121","_211"]]}"""
).to_polygons()
start.polygons[0][0].visual_settings.polygon_color = RED
start.polygons[0][1].visual_settings.polygon_color = RED
start.polygons[0][2].visual_settings.polygon_color = RED
start = start.to_leafs()
tree = PullBackTree.build(start, 1)
polygons = tree.flatten()[1][0].to_polygons().polygons
points = []
for poly in polygons:
    points += poly

print(GapLamination(polygons=[points], points=[], degree=3))


# with open("./rabbit_tree_9.json") as f:
#     tree = custom_parse(f.read())
assert isinstance(tree, PullBackTree)
(G, table) = tree.nx_tree()


graphMob = Graph(
    G.nodes,
    G.edges,
    layout="tree",
    vertex_mobjects=dict(enumerate(map(lambda lam: lam.to_polygons().build(2), table))),
    root_vertex=0,
    layout_scale=9,
)


class CustomTree(Scene):
    def construct(self):
        self.add(graphMob)


A = ceil(graphMob.height)
B = ceil(graphMob.width)
pix = 200
with tempconfig(
    {
        "pixel_height": A * pix,
        "pixel_width": B * pix,
        "frame_height": A,
        "frame_width": B,
        "disable_caching": True,
    }
):
    CustomTree().render()
