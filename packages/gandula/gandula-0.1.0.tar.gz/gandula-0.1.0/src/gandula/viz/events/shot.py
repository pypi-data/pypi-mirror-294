import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from gandula.providers.pff.schema.event import ShootingEvent
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

from ..pitch import Pitch


def plot_shot_map(
    pitch: Pitch,
    shots: list[ShootingEvent] | pd.DataFrame,
    circle: bool = True,
    xg: bool = False,
    distribution: bool = False,
    circle_size: int = 6,
):
    """
    Plot a shot map of the match.

    :param pitch: A Pitch object where the shots will be plotted.
    :param shots: A DataFrame containing shot data with columns 'x', 'y', and optionally 'xg', or a list of PFF Events.
    :param circle: If True, scatter the shots as circles on the pitch.
    :param xg: If True, change the size and color of the shot based on the xG value.
    :param distribution: If True, plot a heatmap of shots on the pitch based on a 52x34 grid.
    """
    if isinstance(shots, list):
        raise NotImplementedError('The function only supports DataFrame inputs.')

    elif isinstance(shots, pd.DataFrame):
        shots = shots.copy()

        # TODO 0.2.0: get shots center of coordinates system
        # TODO 0.2.0: get shots pitch size
        shots.loc[:, 'x'] = shots.loc[:, 'x'] + pitch.width / 2
        shots.loc[:, 'y'] = shots.loc[:, 'y'] + pitch.height / 2

        ax = pitch.draw_pitch()

        if circle:
            if xg:
                sizes = (
                    circle_size + 2 * shots['xg']
                )  # Size goes from circle_size to circle_size + 2
                colors = shots['xg']  # Color corresponds to xG values
                norm = Normalize(vmin=0, vmax=1)
                sm = ScalarMappable(cmap='coolwarm', norm=norm)
                ax.scatter(
                    shots['x'],
                    shots['y'],
                    s=sizes,
                    c=colors,
                    cmap='coolwarm',
                    edgecolor='black',
                    alpha=0.8,
                )
                sm.set_array([])
                cbar = plt.colorbar(sm, ax=ax, orientation='vertical')
                cbar.set_label('xG')
            else:
                ax.scatter(
                    shots['x'], shots['y'], s=6, c='black', edgecolor='white', alpha=0.6
                )

        # Ensure pitch lines and scatter plots are on top
        if circle:
            ax.set_zorder(2)

        if distribution:
            x_bins = np.arange(0, pitch.width + 1)
            y_bins = np.arange(0, pitch.height + 1)
            if xg:
                statistic, _, _ = np.histogram2d(
                    shots['x'], shots['y'], bins=[x_bins, y_bins], weights=shots['xg']
                )
            else:
                statistic, _, _ = np.histogram2d(
                    shots['x'], shots['y'], bins=[x_bins, y_bins]
                )

            plt.imshow(
                statistic.T,
                origin='lower',
                cmap='Blues',
                extent=(0, pitch.width, 0, pitch.height),
                alpha=0.7,
            )
            plt.colorbar(label='Shot Count')

    plt.show()
