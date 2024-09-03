from manim import config

# import ligth_theme # (download from https://gist.github.com/abul4fia/353b9a2c3d000088a82175fa64e0ce24#file-ligth_theme-py)
from manim_lamination_builder import PullBackTree, parse_lamination

start = parse_lamination("""{polygons:[['_100','_010','_001']],degree:2}""")
tree = PullBackTree.build(start, 5)

lams = list(filter(lambda lam: lam.trapped_criticality() == 0, tree.flatten()[-1]))
config.preview = True
tree.show_pullback_tree()

