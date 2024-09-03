from manim import Graph, Scene, config, tempconfig
from math import ceil
from manim_lamination_builder import (
    TreeRender,
    PullBackTree,
    parse_lamination,
    custom_parse,
    custom_dump,
    rabbit_nth_pullback
)

start = rabbit_nth_pullback(10).to_leafs()
tree = PullBackTree.build(start, 2)
# print(len(tree.flaten()[-1]))
print(custom_dump(tree))
