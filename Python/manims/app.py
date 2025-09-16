from manim import *


class SherkMobile(Scene):
    def construct(self):
        # Create Axes (coordinate system)
        sigle = Text("SIL").scale(1.6)
        self.play(Create(sigle))

        self.wait(4)


class GrowingMovingCircle(Scene):
    def construct(self):
        # Create Axes (coordinate system)
        axes = Axes(
            x_range=[-1, 6, 1],  # X-axis range from -1 to 6
            y_range=[-6, 6, 1],  # Y-axis range from -1 to 6
            axis_config={"color": GREEN}
        )

        # Create initial circle at origin with radius 0.5
        circle = Circle(radius=1, color=RED)
        circle.move_to(axes.c2p(0, 0))  # Place at origin

        # Add axes and initial circle
        self.play(Create(axes), Create(circle))
        self.wait(1)

        # Define circle movement (to the right) and growth (radius increases)
        def update_circle(mob, dt):
            mob.shift(RIGHT * dt)  # Move right over time
            mob.scale(1 + 0.125 * dt)  # Scale up the radius

        # Apply updater function
        circle.add_updater(update_circle)

        # Run animation for 5 seconds
        self.wait(5)

        # Stop updating after animation
        circle.remove_updater(update_circle)


class AddTriangle(Scene):
    def construct(self):
        obj = Polygon([0, -1, 0], [0, 3, 0], [3, -1, 0])
        a = Text("a").next_to(obj, LEFT).scale(.7)
        b = Text("b").next_to(obj, DOWN).scale(.7)
        c = Text("c").next_to(obj, RIGHT).scale(.7).shift(LEFT*1.5)
        tringle = VGroup(obj, a, b, c)
        self.play(Create(tringle))
        self.play(tringle[0].animate.set_color(RED))
        self.wait(1)


class PythagoreanTransform(Scene):
    def construct(self):
        # Initial text
        theorem_text = Text(
            "The area of the square whose side is the\nhypotenuse(the side opposite the right\nangle) is equal to the sum of the areas\nof the squares on the other two sides"
        )
        self.play(Write(theorem_text))
        self.wait(1)
        self.play(theorem_text.animate.scale(1.1))
        # Mathematical formula

        # Display text
        obj = Polygon([0, -1, 0], [0, 3, 0], [3, -1, 0])
        a = Text("a").next_to(obj, LEFT).scale(.7)
        b = Text("b").next_to(obj, DOWN).scale(.7)
        c = Text("c").next_to(obj, RIGHT).scale(.7).shift(LEFT*1.5)
        formula = MathTex("a^2 + b^2 = c^2").next_to(obj, RIGHT*8).scale(1.5)
        tringle = VGroup(obj, a, b, c, formula).shift(LEFT*5)
        # Transform text into formula
        self.play(Transform(theorem_text, tringle))
        self.wait(2)


class ReciprocalGraph(Scene):
    def construct(self):
        # Create axes with specific range
        nb = 7
        axes = Axes(
            x_range=[-nb, nb, 1],  # x-axis from -3 to 3
            y_range=[-nb, nb, 1],  # y-axis from -3 to 3
            axis_config={"color": BLUE},
        )

        # Define the function 1/x
        def func(x):
            return x**2+x+3  # Avoid division by zero

        # Plot the function while handling discontinuity at x=0
        graph = axes.plot(func,
                          color=RED)

        # Labels
        labels = axes.get_axis_labels(x_label="x", y_label="f(x)")

        # Title
        title = Text("Graph of f(x) = 1/x").to_edge(UP)

        # Add coordinates at specific points
        points = [
            (-2, func(-2)),  # f(-2)
            (-1, func(-1)),  # f(-1)
            (1, func(1)),    # f(1)
            (2, func(2)),    # f(2)
        ]

        coord_labels = VGroup(
            *[
                Dot(axes.c2p(x, y), color=YELLOW).scale(0.7)  # Dots
                for x, y in points
            ],
            *[
                MathTex("A").next_to(
                    axes.c2p(x, y), UR, buff=0.2)
                for x, y in points
            ]
        )

        # Add everything to the scene
        self.add(axes, labels, graph, coord_labels)
