from manim_lamination_builder import (
    PullBackTree,
    parse_lamination,
    custom_parse,
    custom_dump,
    rabbit_nth_pullback,
)
from manim import config
import ligth_theme

config.preview = True

# start = parse_lamination("""{polygons:[['_10','_01']],degree:3}""").to_leafs()
# start = parse_lamination("""{polygons:[['_100','_010','_001']],degree:3}""").to_leafs()
# with open("./basilica_10.json") as f:
#     tree = custom_parse(f.read())
#     assert isinstance(tree, PullBackTree)
# tree = tree.extend_by_one_level()

# print(custom_dump(tree))
# for lst in tree.flatten():
#     print(len(lst))

# print(len(tree.flaten()[-1]))
# tree.show_pullback_tree()
# print(tree.nx_generation_graph(4)[0])
import numpy as np


def rotate_point(point):
    # rotation angle in radians
    theta = -0.40

    # extract x and y coordinates
    x, y = point[:2]

    # calculate the rotated coordinates
    rotated_x = x * np.cos(theta) - y * np.sin(theta)
    rotated_y = x * np.sin(theta) + y * np.cos(theta)

    # create the new point, preserving the z-coordinate if it exists
    if len(point) == 3:
        return np.array([rotated_x, rotated_y, point[2]])
    else:
        return np.array([rotated_x, rotated_y, 0])


def translate_point(point):
    x, y = point[:2]

    rotated_x = x - 0.5 - 0.2
    rotated_y = y - 0.5

    # Create the new point, preserving the z-coordinate if it exists
    if len(point) == 3:
        return np.array([rotated_x, rotated_y, point[2]])
    else:
        return np.array([rotated_x, rotated_y, 0])


def fixedleaf():
    start = parse_lamination("""{polygons:[['_1','_0']],degree:3}""").to_leafs()
    theta = -0.40

    n = 2
    tree = PullBackTree.build(start, n)
    tree.show_generation_graph(n, trans=rotate_point)


def tryangle():
    start = parse_lamination(
        """{polygons:[['_001','_010','_100']],degree:3}"""
    ).to_leafs()

    n = 2
    tree = PullBackTree.build(start, n)
    tree.show_generation_graph(n, sf=1.8, trans=translate_point)


def line():
    start = parse_lamination("""{polygons:[['_01','_10']],degree:3}""").to_leafs()

    def rotate_point(point):
        # rotation angle in radians
        theta = 0.38

        # extract x and y coordinates
        x, y = point[:2]

        # calculate the rotated coordinates
        rotated_x = x * np.cos(theta) - y * np.sin(theta)
        rotated_y = x * np.sin(theta) + y * np.cos(theta)

        # create the new point, preserving the z-coordinate if it exists
        if len(point) == 3:
            return np.array([rotated_x, rotated_y, point[2]])
        else:
            return np.array([rotated_x, rotated_y, 0])

    n = 2
    tree = PullBackTree.build(start, n)
    tree.show_generation_graph(
        n, sf=1.8, trans=rotate_point
    )  # , sf=1.8, trans=translate_point


start = parse_lamination(
    """{polygons:[], points:['_001','_010','_100','_01','_10','_1','_0'],degree:3}"""
)

for p in start.points:
    print(p.to_faction())

start = parse_lamination("""{polygons:[['_1','_0']],degree:3}""").to_leafs()
start = parse_lamination("""{polygons:[['_001','_010','_100']],degree:3}""").to_leafs()
start = parse_lamination("""{polygons:[['_01','_10']],degree:3}""").to_leafs()


tree = PullBackTree.build(start, 2)
# tree.show_pullback_tree()
