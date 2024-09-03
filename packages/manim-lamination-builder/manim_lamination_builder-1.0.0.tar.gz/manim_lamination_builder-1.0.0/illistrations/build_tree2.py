from manim_lamination_builder import PullBackTree, parse_lamination, custom_dump

start = parse_lamination("""{polygons:[['_100','_010','_001']],degree:3}""").to_leafs()
tree = PullBackTree.build(start, 6)
print(custom_dump(tree))
