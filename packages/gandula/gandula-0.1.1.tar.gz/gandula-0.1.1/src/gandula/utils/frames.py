from gandula.providers.pff.schema.tracking import PFF_Frame
from gandula.providers.pff.schema.tracking import PossessionEventType


def _get_frame_by_possession_type(
    frames: list[PFF_Frame],
    possession_event_type: PossessionEventType,
    enhanced: bool = False,
) -> list[PFF_Frame]:
    """
    Extracts frames that match the given possession event type.
    :param frames: A list of PFF_Frame frames.
    :param possession_event_type: A PossessionEventType enum.
    :return: A list of frames that match the given possession event type.
    """
    return [
        frame
        for frame in frames
        if (
            not enhanced
            and (
                frame.possession
                and frame.possession.possession_event_type == possession_event_type
            )
        )
        or (
            enhanced
            and (
                frame['frame'].possession
                and frame['frame'].possession.possession_event_type
                == possession_event_type
            )
        )
    ]


def get_shot_frames(frames: list[PFF_Frame], enhanced: bool = False) -> list[PFF_Frame]:
    """
    Extracts frames that are shots.

    :param frames: A list of PFF_Frame frames.
    :param enhanced: A boolean to indicate if the frames are enhanced.
    :return: A list of frames that are shots.
    """
    return _get_frame_by_possession_type(
        frames, PossessionEventType.SHOT, enhanced
    )  # TODO: use better solution for enhanced


def get_pass_frames(frames: list[PFF_Frame], enhanced: bool = False) -> list[PFF_Frame]:
    """
    Extracts frames that are passes.
    :param frames: A list of PFF_Frame frames.
    :param enhanced: A boolean to indicate if the frames are enhanced.
    :return: A list of frames that are passes.
    """
    return _get_frame_by_possession_type(
        frames, PossessionEventType.PASS, enhanced
    )  # TODO: use better solution for enhanced


def get_carry_frames(
    frames: list[PFF_Frame], enhanced: bool = False
) -> list[PFF_Frame]:
    """
    Extracts frames that are carries.

    :param frames: A list of PFF_Frame frames.
    :param enhanced: A boolean to indicate if the frames are enhanced.
    :return: A list of frames that are carries.
    """
    return _get_frame_by_possession_type(
        frames, PossessionEventType.BALL_CARRY, enhanced
    )  # TODO: use better solution for enhanced


def get_challenge_frames(
    frames: list[PFF_Frame], enhanced: bool = False
) -> list[PFF_Frame]:
    """
    Extracts frames that are challenges.

    :param frames: A list of PFF_Frame frames.
    :param enhanced: A boolean to indicate if the frames are enhanced.
    :return: A list of frames that are challenges.
    """
    return _get_frame_by_possession_type(
        frames, PossessionEventType.CHALLENGE, enhanced
    )  # TODO: use better solution for enhanced


def get_clearance_frames(
    frames: list[PFF_Frame], enhanced: bool = False
) -> list[PFF_Frame]:
    """
    Extracts frames that are clearances.

    :param frames: A list of PFF_Frame frames.
    :param enhanced: A boolean to indicate if the frames are enhanced.
    :return: A list of frames that are clearances.
    """
    return _get_frame_by_possession_type(
        frames, PossessionEventType.CLEARANCE, enhanced
    )  # TODO: use better solution for enhanced


def get_rebound_frames(
    frames: list[PFF_Frame], enhanced: bool = False
) -> list[PFF_Frame]:
    """
    Extracts frames that are rebounds.

    :param frames: A list of PFF_Frame frames.
    :param enhanced: A boolean to indicate if the frames are enhanced.
    :return: A list of frames that are rebounds.
    """
    return _get_frame_by_possession_type(
        frames, PossessionEventType.REBOUND, enhanced
    )  # TODO: use better solution for enhanced


def get_cross_frames(
    frames: list[PFF_Frame], enhanced: bool = False
) -> list[PFF_Frame]:
    """
    Extracts frames that are crosses.

    :param frames: A list of PFF_Frame frames.
    :param enhanced: A boolean to indicate if the frames are enhanced.
    :return: A list of frames that are crosses.
    """
    return _get_frame_by_possession_type(
        frames, PossessionEventType.CROSS, enhanced
    )  # TODO: use better solution for enhanced


def get_frames_with_events(frames: list[PFF_Frame]) -> list[PFF_Frame]:
    """
    Extracts frames that have events.

    :param frames: A list of PFF_Frame frames.
    :return: A list of frames that have events.
    """
    return [frame for frame in frames if frame.event_id]


def get_frames_with_events_dict(frames: list[PFF_Frame]) -> dict[str, list[PFF_Frame]]:
    """
    Extracts frames that have events and returns a dictionary with the event_id as key and a list of frames as value.

    :param frames: A list of PFF_Frame frames.
    :return: A dictionary with the event_id as key and a list of frames as value.
    """
    frames_with_events: dict[str, list[PFF_Frame]] = {}

    for frame in frames:
        if frame.event_id:
            event_id_str = str(frame.event_id)
            if event_id_str not in frames_with_events:
                frames_with_events[event_id_str] = []
            frames_with_events[event_id_str].append(frame)

    return frames_with_events
