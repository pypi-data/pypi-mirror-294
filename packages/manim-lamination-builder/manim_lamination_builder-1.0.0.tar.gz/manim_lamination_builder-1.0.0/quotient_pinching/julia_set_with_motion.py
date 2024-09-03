from manim import *
from manim_lamination_builder import rabbit_nth_pullback

config.frame_width /= 3
config.frame_height /= 3


class OpeningStill(Scene):
    def construct(self):
        img = ImageMobject("julia_set.png")
        img.width = 3
        img.height = 3
        img.move_to(LEFT * 1.1 + DOWN * 0.2)
        lammob = rabbit_nth_pullback(12).build()
        lammob.move_to(RIGHT * 1.1 + DOWN * 0.2)
        self.add(img)
        self.add(lammob)

        text2 = Text("Lamination", font_size=20)
        text2.next_to(lammob, UP)
        self.add(text2)

        text1 = Text("Julia set", font_size=20)
        text1.next_to(img, UP)
        text1.shift(0.5316406250000001 * DOWN)
        self.add(text1)


fixed_point = -0.276337623593117 * RIGHT + 0.479727984309391 * UP

from psi import apply_complex_function, f, f0


class JuliaSetWithMotion(Scene):
    def construct(self):
        label = MathTex("z \\mapsto z^2 - 0.13 + 0.74i", font_size=16).move_to(
            UP + RIGHT * 1.2
        )
        label.z_index = 1
        self.add(label)
        img = ImageMobject("julia_set.png")
        img.width = 4
        img.height = 4
        self.add(img)
        dots = VGroup(
            Dot(ORIGIN + 0.5 * fixed_point),
            Dot(ORIGIN),
            Dot(UP),
            Dot(RIGHT),
            Dot(1.272199318 * RIGHT - 0.5086157 * UP),
        )
        for dot in dots:
            dot.scale_to_fit_width(0.04)
        self.add(dots)
        self.wait(0.7)
        for _ in range(10):
            end = apply_complex_function(dots, f)
            for dot in end:
                dot.scale_to_fit_width(0.04)
            self.play(Transform(dots, end))
            self.remove(dots)
            dots = end
            self.add(dots)
            self.wait(0.7)


img = ImageMobject("julia_set.png")
img.width = 4
img.height = 4


class JuliaSetWithFixedPoint(Scene):
    def construct(self):
        fixed_point = -0.276337623593117 * RIGHT + 0.479727984309391 * UP
        self.add(img)
        label = MathTex("z \\mapsto z^2 - 0.13 + 0.74i", font_size=16).move_to(
            UP + RIGHT * 1.2
        )
        self.add(label)
        label_fixed = MathTex("-0.276 + 0.479i", font_size=16).move_to(fixed_point + RIGHT*0.8)
        self.add(label_fixed)
        self.add(Dot(fixed_point,radius=DEFAULT_DOT_RADIUS/3, color=RED))

class JuliaSetWithAndPre(Scene):
    def construct(self):
        fixed_point = -0.276337623593117 * RIGHT + 0.479727984309391 * UP
        self.add(img)
        label = MathTex("z \\mapsto z^2 - 0.13 + 0.74i", font_size=16).move_to(
            UP + RIGHT * 1.2
        )
        self.add(label)
        label_fixed = MathTex("-0.276 + 0.479i", font_size=16).move_to(fixed_point + RIGHT*0.8)
        self.add(label_fixed)
        self.add(Dot(fixed_point,radius=DEFAULT_DOT_RADIUS/3, color=RED))
        self.add(Dot(-fixed_point,radius=DEFAULT_DOT_RADIUS/3, color=RED))

config.preview = True
# config.quality = "low_quality"
JuliaSetWithFixedPoint().render()
