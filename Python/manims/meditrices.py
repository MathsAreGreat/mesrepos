from manim import *


class TrianglePerpendicularBisectorsSimplified(Scene):
    def construct(self):
        # Define vertices of the triangle
        A = np.array([-3.0, 3.0, 0.0])
        B = np.array([3.0, 3.0, 0.0])
        C = np.array([1.0, -2.0, 0.0])

        # Draw the triangle
        triangle = Polygon(A, B, C, color=BLUE)

        # Draw perpendicular bisectors
        bisector_AB = self.perpendicular_bisector(A, B)
        bisector_BC = self.perpendicular_bisector(B, C)
        bisector_CA = self.perpendicular_bisector(C, A)

        # Label vertices
        labels = VGroup(
            MathTex("A").next_to(A, LEFT),
            MathTex("B").next_to(B, RIGHT),
            MathTex("C").next_to(C, DOWN)
        )
# Find and display the circumcenter
        circumcenter = self.find_intersection(A, B, C)
        circumcenter_dot = Dot(circumcenter, color=YELLOW)

        self.play(Create(triangle))

        self.play(Write(labels))

        self.play(Create(bisector_AB), Create(
            bisector_BC), Create(bisector_CA))

        # Add perpendicular symbols
        self.add_right_angle_symbol(A, B)
        self.add_right_angle_symbol(B, C)
        self.add_right_angle_symbol(C, A)

        self.play(Create(circumcenter_dot))
        self.play(Write(MathTex("O").next_to(circumcenter_dot, UP)))

        self.wait()

    def perpendicular_bisector(self, point1, point2):
        # Calculate the midpoint
        midpoint = (point1 + point2) / 2

        # Direction vector of the segment
        direction = point2 - point1

        # Perpendicular vector
        perpendicular_direction = np.array([-direction[1], direction[0], 0])
        perpendicular_direction /= np.linalg.norm(perpendicular_direction)

        # Extend the bisector
        start = midpoint - perpendicular_direction * 5
        end = midpoint + perpendicular_direction * 5
        return Line(start, end, color=GREEN)

    def add_right_angle_symbol(self, point1, point2):
        # Calculate the midpoint
        midpoint = (point1 + point2) / 2

        # Direction vector
        direction = point2 - point1

        # Perpendicular vector
        perpendicular_direction = np.array([-direction[1], direction[0], 0])
        perpendicular_direction /= np.linalg.norm(perpendicular_direction)

        # Create the right-angle symbol
        right_angle = RightAngle(
            Line(midpoint, midpoint + direction / 2),
            Line(midpoint, midpoint + perpendicular_direction / 2),
            length=0.3
        )
        self.play(Create(right_angle))

    def find_intersection(self, A, B, C):
        # Midpoints
        midpoint_AB = (A + B) / 2
        midpoint_BC = (B + C) / 2

        # Directions
        dir_AB = np.array([-(B - A)[1], (B - A)[0]])
        dir_BC = np.array([-(C - B)[1], (C - B)[0]])

        # Solve for t
        numerator = np.cross(midpoint_BC[:2] - midpoint_AB[:2], dir_BC)
        denominator = np.cross(dir_AB, dir_BC)

        if denominator == 0:
            raise ValueError(
                "The perpendicular bisectors are parallel and do not intersect.")

        t = numerator / denominator
        circumcenter = midpoint_AB + t * \
            np.append(dir_AB, 0)  # Add 0 for z-coordinate
        return circumcenter
