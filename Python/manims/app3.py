from manim import *


class TriangleWithMedians(Scene):
    def construct(self):
        # Define triangle vertices
        A = [-4, -1, 0]
        B = [4, -3, 0]
        C = [1, 3, 0]

        # Create triangle
        triangle = Polygon(A, B, C, color=BLUE)

        # Calculate midpoints
        M_AB = [(A[0] + B[0]) / 2, (A[1] + B[1]) / 2, 0]
        M_BC = [(B[0] + C[0]) / 2, (B[1] + C[1]) / 2, 0]
        M_CA = [(C[0] + A[0]) / 2, (C[1] + A[1]) / 2, 0]
        # Create medians
        median_A = Line(A, M_BC, color=YELLOW_E)
        median_B = Line(B, M_CA, color=YELLOW_E)
        median_C = Line(C, M_AB, color=YELLOW_E)

        # Find centroid (intersection of medians)
        centroid = [(A[0] + B[0] + C[0]) / 3, (A[1] + B[1] + C[1]) / 3, 0]
        centroid_dot = Dot(centroid, color=YELLOW)
        centroid_label = MathTex("G").next_to(centroid_dot, DR, buff=0.2)

        # Midpoint dots
        midpoints = VGroup(
            Dot(M_AB, color=GREEN),
            Dot(M_BC, color=GREEN),
            Dot(M_CA, color=GREEN),
        )

        # Labels for vertices
        labels = VGroup(
            MathTex("A").next_to(A, UL, buff=0.2),
            MathTex("B").next_to(B, DR, buff=0.2),
            MathTex("C").next_to(C, UR, buff=0.2),
        )

        # Add all elements to scene
        self.add(triangle, median_A, median_B, median_C,
                 midpoints, centroid_dot, centroid_label, labels)
