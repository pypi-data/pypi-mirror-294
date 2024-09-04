from typing import Literal

from .auth import validate_api_key as validate_api_key
from .competition import get_available_competitions as get_available_competitions
from .competition import get_competition as get_competition
from .competition import get_competitions as get_competitions
from .match import get_enhanced_frames as get_enhanced_frames
from .match import get_frames as get_frames
from .match import get_match as get_match
from .match import get_match_event as get_match_event
from .match import get_match_events as get_match_events
from .providers.pff.local import loader as loader
from .providers.pff.schema.event import PFF_Event
from .providers.pff.schema.event import PFF_PossessionEvent
from .providers.pff.schema.tracking import PFF_Frame
from .viz.animation import animate as animate
from .viz.events.shot import plot_shot_map as plot_shot_map
from .viz.frame import view_frame as view_frame
from .viz.pitch import Pitch as Pitch


def __repr__() -> str:
    return 'Gandula Library'


def _repr_html_() -> str:
    return (
        '<h1>Gandula</h1>'
        '<p>Library for interacting and manipulating PFF data</p>'
        '<h2>API</h2>'
        '<ul>'
        '<li>gandula.validate_api_key</li>'
        '<li>gandula.get_available_competitions</li>'
        '<li>gandula.get_match_events</li>'
        '<li>gandula.get_competitions</li>'
        '<li>gandula.get_frames</li>'
        '<li>gandula.get_enhanced_frames</li>'
        '<li>gandula.view</li>'
        '<li>gandula.animate</li>'
        '</ul>'
    )


AvailableFormats = Literal['dict', 'json', 'dataframe']


def view(
    gandula_obj: PFF_Frame | PFF_PossessionEvent | PFF_Event,
    fmt: AvailableFormats | None = None,
):
    if isinstance(gandula_obj, PFF_Frame) and fmt is None:
        pitch = Pitch(pitch_color='white', fig_size=(15, 10), line_color='black')
        pitch.draw_pitch()
        return view_frame(gandula_obj, pitch=pitch)

    if fmt is None:
        fmt = 'dict'

    if fmt == 'dict':
        return gandula_obj.model_dump(
            exclude_none=True, exclude_unset=True, exclude_defaults=True
        )
    elif fmt == 'json':
        return gandula_obj.model_dump_json(
            exclude_none=True, exclude_unset=True, exclude_defaults=True
        )
    elif fmt == 'dataframe':
        from pandas import DataFrame

        return DataFrame(gandula_obj)
