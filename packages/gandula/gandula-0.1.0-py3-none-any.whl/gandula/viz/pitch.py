import matplotlib.patches as patches
import matplotlib.pyplot as plt


class Pitch:
    def __init__(
        self,
        width=105,
        height=68,
        fig_size=(12, 8),
        pitch_color='white',
        line_color='black',
        margin=5,
    ):
        self.width = width
        self.height = height
        self.fig, self.ax = plt.subplots(figsize=fig_size)
        self.pitch_color = pitch_color
        self.line_color = line_color
        self.margin = margin

    def draw_pitch(self):
        # Clear the axes
        self.ax.clear()
        self.ax.set_facecolor(self.pitch_color)

        # Pitch Outline & Centre Line
        self.ax.plot(
            [0, 0, self.width, self.width, 0],
            [0, self.height, self.height, 0, 0],
            color=self.line_color,
        )
        self.ax.plot(
            [self.width / 2, self.width / 2], [0, self.height], color=self.line_color
        )

        # Left Penalty Area
        self.ax.plot(
            [0, 16.5, 16.5, 0], [13.2, 13.2, 54.8, 54.8], color=self.line_color
        )
        # Right Penalty Area
        self.ax.plot(
            [self.width, self.width - 16.5, self.width - 16.5, self.width],
            [13.2, 13.2, 54.8, 54.8],
            color=self.line_color,
        )

        # Left 6-yard Box
        self.ax.plot([0, 5.5, 5.5, 0], [24.2, 24.2, 43.8, 43.8], color=self.line_color)
        # Right 6-yard Box
        self.ax.plot(
            [self.width, self.width - 5.5, self.width - 5.5, self.width],
            [24.2, 24.2, 43.8, 43.8],
            color=self.line_color,
        )

        # Centre Circle and Centre Spot
        centre_circle = patches.Circle(
            (self.width / 2, self.height / 2), 9.15, color=self.line_color, fill=False
        )
        centre_spot = patches.Circle(
            (self.width / 2, self.height / 2), 0.5, color=self.line_color
        )
        self.ax.add_patch(centre_circle)
        self.ax.add_patch(centre_spot)

        # Penalty Spots and Arcs around penalty areas
        left_penalty_spot = patches.Circle(
            (11, self.height / 2), 0.5, color=self.line_color
        )
        right_penalty_spot = patches.Circle(
            (self.width - 11, self.height / 2), 0.5, color=self.line_color
        )
        self.ax.add_patch(left_penalty_spot)
        self.ax.add_patch(right_penalty_spot)

        # Arcs around penalty area
        left_arc = patches.Arc(
            (11, self.height / 2),
            height=18.3,
            width=18.3,
            angle=0,
            theta1=308,
            theta2=52,
            color=self.line_color,
        )
        right_arc = patches.Arc(
            (self.width - 11, self.height / 2),
            height=18.3,
            width=18.3,
            angle=0,
            theta1=128,
            theta2=232,
            color=self.line_color,
        )
        self.ax.add_patch(left_arc)
        self.ax.add_patch(right_arc)

        # Tidy Axes
        self.ax.set_xticks([])
        self.ax.set_yticks([])

        # Set the limits
        self.ax.set_xlim(-self.margin, self.width + self.margin)
        self.ax.set_ylim(-self.margin, self.height + self.margin)

        return self.ax
