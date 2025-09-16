from manim import *


class TangentToCircle(Scene):
    def construct(self):
        # Radius and points setup
        radius = 3
        O = ORIGIN  # Center of the circle
        B = RIGHT * radius  # Point B on the circle (diameter endpoint)
        C = LEFT * radius  # Point C on the circle (diameter endpoint)

        # Angle setup
        angle_AOB = 85 * DEGREES
        A = rotate_vector(B, angle_AOB, axis=IN)  # Point A based on the angle

        # Draw the circle
        circle = Circle(radius=radius, color=BLUE)

        # Draw points
        O_dot = Dot(O, color=YELLOW)
        B_dot = Dot(B, color=RED)
        C_dot = Dot(C, color=RED)
        A_dot = Dot(A, color=GREEN)

        # Draw labels
        O_label = MathTex("O").next_to(O, UP)
        B_label = MathTex("B").next_to(B, RIGHT)
        C_label = MathTex("C").next_to(C, LEFT)
        A_label = MathTex("A").next_to(A, DOWN)

        # Draw lines
        diameter = Line(C, B, color=PURPLE)
        radius_OA = Line(O, A, color=ORANGE)
        radius_AC = Line(C, A, color=RED)

        # Draw tangent (perpendicular to radius at A)
        tangent_direction = normalize(rotate_vector(
            A - O, PI / 2))  # Perpendicular direction
        tangent = Line(A - tangent_direction * 3, A +
                       tangent_direction * 3, color=GREEN)

        # Angle arc and label
        angle_arc = Arc(start_angle=Line(O, A).get_angle(),
                        angle=angle_AOB,
                        radius=0.5, color=WHITE)
        angles_arc = Arc(start_angle=Line(A, C).get_angle(),
                         angle=-Line(C, A).get_angle()+tangent.get_angle(),
                         radius=0.5, color=YELLOW, arc_center=A)
        angle_label = MathTex("85^\circ").next_to(
            angle_arc, DOWN+RIGHT, buff=0.1)

        # Add elements to the scene
        self.play(Create(circle))
        self.play(Create(diameter), Create(radius_OA))
        self.play(Create(tangent))
        self.play(
            Create(radius_AC),
            Create(angles_arc),
            FadeIn(O_dot, B_dot, C_dot, A_dot),
            Write(O_label),
            Write(B_label),
            Write(C_label),
            Write(A_label),
            Create(angle_arc),
            Write(angle_label)
        )

        # Keep the scene
        self.wait(2)
        question = Tex("Calculer $\widehat{EAB}$ :").to_corner(UL)
        self.play(Create(question))
        self.wait(2)


class HeronScene(ThreeDScene):
    def construct(self):
        # Create a triangle with side labels
        triangle = Polygon(
            [0, 0, 0],
            [-2, -3, 0],
            [3, -3, 0],
            color=WHITE
        )
        # Create a triangle with side labels
        triangle1 = Polygon(
            [0, 0, 0], [-2, 3, 0], [3, 3, 0], color=BLUE
        )
        self.play(
            GrowFromCenter(triangle1)
        )
