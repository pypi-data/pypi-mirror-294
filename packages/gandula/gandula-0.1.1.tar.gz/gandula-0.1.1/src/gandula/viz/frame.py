from gandula.providers.pff.schema.tracking import PFF_Frame

from .pitch import Pitch


def view_frame(
    frame: PFF_Frame,
    pitch: Pitch,
    kalman_filter: bool = False,
    team_colors: tuple = ('ro', 'bo'),
    ball_color: str = 'wo',
    player_markersize: int = 12,
    ball_markersize: int = 7,
    show_jersey_number: bool = True,
    jersey_number_color: str = 'white',
) -> Pitch:
    ax = pitch.ax

    # draw players
    home_players = (
        frame.home_players_with_kalman if kalman_filter else frame.home_players
    )
    away_players = (
        frame.away_players_with_kalman if kalman_filter else frame.away_players
    )
    for player in home_players:
        # TODO: integrate with PR related to pitch coordinates
        ax.plot(
            player.x + 105 / 2,
            player.y + 68 / 2,
            team_colors[0],
            markersize=player_markersize,
        )
        if show_jersey_number:
            ax.text(
                player.x + 105 / 2,
                player.y + 68 / 2,
                str(player.jersey),
                color=jersey_number_color,
                ha='center',
                va='center',
                fontsize=player_markersize - 2,
            )
    for player in away_players:
        # TODO: integrate with PR related to pitch coordinates
        ax.plot(
            player.x + 105 / 2,
            player.y + 68 / 2,
            team_colors[1],
            markersize=player_markersize,
        )
        if show_jersey_number:
            ax.text(
                player.x + 105 / 2,
                player.y + 68 / 2,
                str(player.jersey),
                color=jersey_number_color,
                ha='center',
                va='center',
                fontsize=player_markersize - 2,
            )

    # draw ball
    ball = frame.ball_with_kalman if kalman_filter else frame.ball[0]
    if ball is not None:
        ax.plot(
            ball.x + 105 / 2,
            ball.y + 68 / 2,
            ball_color,
            markersize=ball_markersize,
            lw=2,
            markeredgecolor='black',
        )

    return ax
