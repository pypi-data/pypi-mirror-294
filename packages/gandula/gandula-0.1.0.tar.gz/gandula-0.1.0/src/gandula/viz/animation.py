import matplotlib.animation as animation

from gandula.providers.pff.schema.tracking import PFF_Frame

from .frame import view_frame
from .pitch import Pitch


def animate(
    frames: list[PFF_Frame],
    pitch: Pitch,
    output_file: str | None = None,
    kalman_filter: bool = False,
    team_colors: tuple = ('ro', 'bo'),
    ball_color: str = 'wo',
    player_markersize: int = 10,
    ball_markersize: int = 7,
    show_jersey_number: bool = False,
    jersey_number_color: str = 'white',
):
    fig, _ = pitch.fig, pitch.ax

    def _frames(i):
        pitch.draw_pitch()
        view_frame(
            pitch,
            frames[i],
            kalman_filter=kalman_filter,
            team_colors=team_colors,
            ball_color=ball_color,
            player_markersize=player_markersize,
            ball_markersize=ball_markersize,
            show_jersey_number=show_jersey_number,
            jersey_number_color=jersey_number_color,
        )

    ani = animation.FuncAnimation(fig, _frames, frames=len(frames), interval=100)
    if output_file:
        ani.save(output_file, writer='imagemagick')

    return ani
