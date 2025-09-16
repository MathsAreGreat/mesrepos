from manim import *


class TriangleAngleBisectors(Scene):
    def construct(self):
        # Define vertices of the triangle
        # Define vertices of the triangle (ensure floats by using 0.0)
        A = np.array([-3.0, 1.0, 0.0])
        B = np.array([3.0, 1.0, 0.0])
        C = np.array([1.0, -2.0, 0.0])

        # Draw the triangle
        triangle = Polygon(A, B, C, color=BLUE)
        self.play(Create(triangle))

        # Calculate the angle bisectors
        bisector_A = self.angle_bisector(A, B, C)
        bisector_B = self.angle_bisector(B, A, C)
        bisector_C = self.angle_bisector(C, A, B)
        label_A = MathTex("A").next_to(A, LEFT)
        label_B = MathTex("B").next_to(B, RIGHT)
        label_C = MathTex("C").next_to(C, DOWN)
        self.play(Write(label_A), Write(label_B), Write(label_C))
        # Draw angle bisectors
        self.play(Create(bisector_A), Create(bisector_B), Create(bisector_C))

        # Label vertices

        # Calculate and display the incenter
        incenter = self.find_incenter(A, B, C)
        incenter_dot = Dot(incenter, color=YELLOW)
        self.play(Create(incenter_dot))
        self.play(Write(MathTex("I").next_to(incenter_dot, UP)))

        self.wait()

    def angle_bisector(self, vertex, point1, point2):
        """
        Calculate the angle bisector from a vertex to the opposite side.
        The bisector divides the angle at `vertex` into two equal parts.
        """
        # Vector directions
        vec1 = point1 - vertex
        vec2 = point2 - vertex

        # Normalize the vectors
        vec1 /= np.linalg.norm(vec1)
        vec2 /= np.linalg.norm(vec2)

        # Compute the direction of the bisector
        bisector_dir = vec1 + vec2
        bisector_dir /= np.linalg.norm(bisector_dir)

        # Extend the bisector to intersect the opposite side
        return Line(vertex, vertex + bisector_dir * 5, color=GREEN)

    def find_incenter(self, A, B, C):
        """
        Compute the incenter of the triangle using weighted average of vertices
        based on edge lengths.
        """
        # Lengths of the triangle's sides
        a = np.linalg.norm(B - C)
        b = np.linalg.norm(A - C)
        c = np.linalg.norm(A - B)

        # Weighted average of the vertices
        return (a * A + b * B + c * C) / (a + b + c)
