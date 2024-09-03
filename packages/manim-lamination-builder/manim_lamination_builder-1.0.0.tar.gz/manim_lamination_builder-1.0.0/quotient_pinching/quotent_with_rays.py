from manim import BLACK, WHITE, Create, Line
from manim.animation.animation import config
from manim_lamination_builder import rabbit_nth_pullback
from cheating_quotent import CheatingPinch
from psi import apply_complex_function, psi
import numpy as np

config.preview = True
config.frame_width /= 3
config.frame_height /= 3


class MultiScene(CheatingPinch):
    def __init__(self):
        lamination = rabbit_nth_pullback(5)
        super().__init__(lamination)

    def construct(self):
        super().construct()
        for theta in [
            2 * np.pi * 1 / 7,
            2 * np.pi * 2 / 7,
            2 * np.pi * 4 / 7,
        ]:
            line_end = 1.00000000001 * np.array([np.cos(theta), np.sin(theta), 0])
            line = Line(line_end * 2.4, line_end,stroke_width=2)
            line.init_points()
            line.insert_n_curves(100)
            self.play(Create(apply_complex_function(line,psi)))
        self.wait(3)


MultiScene().render()
