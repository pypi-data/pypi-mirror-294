from math import ceil
from manim_lamination_builder import (
    PullBackTree,
    parse_lamination,
    custom_parse,
    custom_dump,
    rabbit_nth_pullback,
)
from manim import PI, Arrow, Group, MathTex, Scene, Tex, config, tempconfig
import ligth_theme
from numpy import inf

from manim_lamination_builder.points import FloatWrapper
from manim_lamination_builder.pull_backs import CriticalTree

config.preview = True
lams = [rabbit_nth_pullback(0)]
assert 1 == len(lams[0].to_polygons().polygons)
schem = CriticalTree(
    first_ccw_end_point=FloatWrapper(1 / 8, 2),
    first_end_point_on_inside=True,
)
for _ in range(8):
    lams.append(schem.pull_back1(lams[-1]))

mobs = sum([[lam.build(2), Arrow().rotate(PI)] for lam in lams], [])[:-1] + [
    MathTex("\dots").scale(3)
]

group = Group(*mobs).arrange_in_grid(rows=2)


class Sequence(Scene):
    def construct(self):
        self.add(group)


top, bot, right, left = -inf, inf, -inf, inf
for mob in mobs:
    top, right = max(top, mob.get_top()[1]), max(right, mob.get_right()[0])
    bot, left = min(bot, mob.get_bottom()[1]), min(left, mob.get_left()[0])
pix = 400
buf = 0  # 0.05
A = ceil(top - bot + 2 * buf)
B = ceil(right - left + 2 * buf)
# graphMob.shift((top + bot) * DOWN + (left + right) * RIGHT)

with tempconfig(
    {
        # "preview": True,
        "pixel_height": A * pix,
        "pixel_width": B * pix,
        "frame_height": A,
        "frame_width": B,
        "disable_caching": True,
        # "top": (top + buf) * UP,
        # "left_size": left - buf,
    }
):
    Sequence().render()
