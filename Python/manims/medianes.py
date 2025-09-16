from manim import *


class TriangleAllMedians(Scene):
    def construct(self):
        # Step 1: Create the triangle
        triangle = Polygon(
            [-3, -2, 0],  # Point A
            [3, -2, 0],   # Point B
            [1, 2, 0],    # Point C
            color=BLUE
        ).set_fill(BLUE, opacity=0.3)

        # Add labels for the vertices
        A_label = MathTex("A").next_to(triangle.get_vertices()[0], LEFT)
        B_label = MathTex("B").next_to(triangle.get_vertices()[1], RIGHT)
        C_label = MathTex("C").next_to(triangle.get_vertices()[2], UP)

        # Step 2: Display the triangle and labels
        self.play(Create(triangle))
        self.play(Write(A_label), Write(B_label), Write(C_label))
        self.wait()

        # Step 3: Construct all three medians
        A, B, C = triangle.get_vertices()

        # Midpoints of the sides
        midpoint_AB = (A + B) / 2
        midpoint_BC = (B + C) / 2
        midpoint_CA = (C + A) / 2

        # Median lines
        # From C to midpoint of AB
        median_CA = Line(midpoint_AB, C, color=GREEN)
        # From A to midpoint of BC
        median_BA = Line(midpoint_BC, A, color=ORANGE)
        # From B to midpoint of CA
        median_CB = Line(midpoint_CA, B, color=PURPLE)

        # Midpoint dots
        midpoint_AB_dot = Dot(midpoint_AB, color=RED)
        midpoint_BC_dot = Dot(midpoint_BC, color=RED)
        midpoint_CA_dot = Dot(midpoint_CA, color=RED)

        # Labels for the midpoints
        M1_label = MathTex("M_1").next_to(midpoint_AB, DOWN)
        M2_label = MathTex("M_2").next_to(midpoint_BC, RIGHT)
        M3_label = MathTex("M_3").next_to(midpoint_CA, LEFT)

        # Animate midpoints and first median
        self.play(FadeIn(midpoint_AB_dot), Write(M1_label))
        self.play(Create(median_CA))
        self.wait()

        # Animate second median
        self.play(FadeIn(midpoint_BC_dot), Write(M2_label))
        self.play(Create(median_BA))
        self.wait()

        # Animate third median
        self.play(FadeIn(midpoint_CA_dot), Write(M3_label))
        self.play(Create(median_CB))
        self.wait()

        # Step 4: Highlight the centroid
        centroid = Dot((A + B + C) / 3, color=YELLOW).scale(1.5)
        centroid_label = MathTex("G").next_to(centroid, 2*RIGHT)

        self.play(FadeIn(centroid), Write(centroid_label))
        self.wait()

        # Step 5: Emphasize the centroid intersection
        explanation = Text(
            "The centroid (G) is where all medians intersect", font_size=24).to_edge(DOWN)
        self.play(Write(explanation))
        self.wait()

        # Step 6: Fade out everything
        self.play(
            *[FadeOut(mob) for mob in [triangle, A_label, B_label, C_label,
                                       midpoint_AB_dot, midpoint_BC_dot, midpoint_CA_dot,
                                       M1_label, M2_label, M3_label,
                                       median_CA, median_BA, median_CB,
                                       centroid, centroid_label, explanation]]
        )
