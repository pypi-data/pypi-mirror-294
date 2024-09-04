from gandula.providers.pff.schema.event import PFF_Event
from gandula.providers.pff.schema.event import PFF_Game
from gandula.providers.pff.schema.event import PFF_PossessionEvent
from gandula.providers.pff.schema.event import Roster
from gandula.providers.pff.schema.tracking import PFF_Frame


def get_next_pass_in_possesssion(
    possession_events: list[PFF_PossessionEvent],
) -> PFF_PossessionEvent:
    return next(event for event in possession_events if event.passingEvent)


def get_next_shot_in_possesssion(
    possession_events: list[PFF_PossessionEvent],
) -> PFF_PossessionEvent:
    return next(event for event in possession_events if event.shootingEvent)


def extract_shots_from_events(events: list[PFF_Event]) -> list[PFF_PossessionEvent]:
    """
    Extracts and returns only events that are shots.

    :param events: A list of PFF_Event objects.
    :return: A list of PFF_Event objects that include shooting events.
    """
    possessions_with_shots = [
        event.possessionEvents
        for event in events
        if event.possessionEvents
        and any(evt.shootingEvent for evt in event.possessionEvents)
    ]
    return [
        get_next_shot_in_possesssion(possessesion)
        for possessesion in possessions_with_shots
    ]


def extract_passes_from_events(events: list[PFF_Event]) -> list[PFF_PossessionEvent]:
    """
    Extracts and returns only events that are passes.

    :param events: A list of PFF_Event objects.
    :return: A list of PFF_Event objects that include passing events.
    """
    possessions_with_passes = [
        event.possessionEvents
        for event in events
        if event.possessionEvents
        and any(evt.passingEvent for evt in event.possessionEvents)
    ]
    return [
        get_next_pass_in_possesssion(possessesion)
        for possessesion in possessions_with_passes
    ]


def match_frames_with_events(
    frames: list[PFF_Frame], events: list[PFF_PossessionEvent]
) -> list[tuple[PFF_PossessionEvent, PFF_Frame]]:
    """
    Extracts frames that match the given possession events and returns a list of tuples containing the event and corresponding frame.

    :param frames: A list of PFF_Frame frames.
    :param events: A list of PFF_PossessionEvent events.
    :return: A list of tuples, each containing a PFF_PossessionEvent and its matching PFF_Frame.
    """
    possession_id_to_event = {event.id: event for event in events}
    return [
        (possession_id_to_event[str(frame.possession_id)], frame)
        for frame in frames
        if frame.possession_id and str(frame.possession_id) in possession_id_to_event
    ]


def rosters_to_dict(rosters: list[Roster]) -> dict[str, int]:
    return {entry.player.id: int(entry.shirtNumber) for entry in rosters}


def _add_shot_coordinates(
    bundled_events_frames: list[tuple[PFF_PossessionEvent, PFF_Frame]],
    player_list: dict[str, int],
) -> list[tuple[PFF_PossessionEvent, PFF_Frame]]:
    for event, frame in bundled_events_frames:
        shooter = player_list.get(event.shootingEvent.shooterPlayer.id)
        shooter_x, shooter_y = frame.get_player_coordinates(shooter, frame.home_ball)
        event.shootingEvent.shotPointX = shooter_x
        event.shootingEvent.shotPointY = shooter_y
    return bundled_events_frames


def update_player_coordinates(
    player, event, attribute_prefix, frame, player_list, is_home
):
    if player:
        player_obj = player_list.get(player.id)
        if player_obj:
            try:
                x, y = frame.get_player_coordinates(player_obj, is_home)
                setattr(event, f'{attribute_prefix}PointX', x)
                setattr(event, f'{attribute_prefix}PointY', y)
            except StopIteration:
                try:
                    x, y = frame.get_player_coordinates(player_obj, not is_home)
                    setattr(event, f'{attribute_prefix}PointX', x)
                    setattr(event, f'{attribute_prefix}PointY', y)
                except StopIteration:
                    print(
                        f'Player {player.id} ({attribute_prefix}) not found in frame {frame.frame_id}'
                    )
                    return


pass_coordinates_to_set = [
    {'attribute_prefix': 'pass', 'player_prefix': 'passer', 'keep_team': True},
    {'attribute_prefix': 'target', 'player_prefix': 'target', 'keep_team': True},
    {'attribute_prefix': 'receiver', 'player_prefix': 'receiver', 'keep_team': True},
    {'attribute_prefix': 'defender', 'player_prefix': 'defender', 'keep_team': False},
    {
        'attribute_prefix': 'failedIntervention',
        'player_prefix': 'failedIntervention',
        'keep_team': False,
    },
    {
        'attribute_prefix': 'missedTouch',
        'player_prefix': 'missedTouch',
        'keep_team': False,
    },
]


def _add_pass_coordinates(
    bundled_events_frames: list[tuple[PFF_PossessionEvent, PFF_Frame]],
    player_list: dict[str, int],
) -> list[tuple[PFF_PossessionEvent, PFF_Frame]]:
    # set player coordinates
    for event, frame in bundled_events_frames:
        for attr_coord in pass_coordinates_to_set:
            is_home = (
                frame.home_ball if attr_coord['keep_team'] else not frame.home_ball
            )
            attribute_prefix = attr_coord['attribute_prefix']
            player_attribute = f"{attr_coord['player_prefix']}Player"

            player = getattr(event.passingEvent, player_attribute)
            update_player_coordinates(
                player,
                event.passingEvent,
                attribute_prefix,
                frame,
                player_list,
                is_home,
            )

    # set end coordinates based on outcome
    return bundled_events_frames


def add_pass_coordinates(pff_match: PFF_Game, frames: list[PFF_Frame]):
    events = pff_match.gameEvents
    passes = extract_passes_from_events(events)
    player_list = rosters_to_dict(pff_match.rosters)
    combined_events_frames = match_frames_with_events(frames, passes)

    combined_with_coordinates = _add_pass_coordinates(
        combined_events_frames, player_list
    )

    enhanced_frames = {}
    for event, frame in combined_with_coordinates:
        enhanced_frames[str(frame.frame_id)] = {'frame': frame, 'event': event}

    return enhanced_frames


def add_shot_coordinates(pff_match: PFF_Game, frames: list[PFF_Frame]):
    events = pff_match.gameEvents
    shots = extract_shots_from_events(events)
    player_list = rosters_to_dict(pff_match.rosters)
    combined_events_frames = match_frames_with_events(frames, shots)

    combined_with_coordinates = _add_shot_coordinates(
        combined_events_frames, player_list
    )

    enhanced_frames = {}
    for event, frame in combined_with_coordinates:
        enhanced_frames[str(frame.frame_id)] = {'frame': frame, 'event': event}

    return enhanced_frames


def add_challenge_coordinates(
    events: list[PFF_Event], frames: list[PFF_Frame]
) -> dict: ...


def add_rebound_coordinates(
    events: list[PFF_Event], frames: list[PFF_Frame]
) -> dict: ...


def add_clearance_coordinates(
    events: list[PFF_Event], frames: list[PFF_Frame]
) -> dict: ...


def add_cross_coordinates(events: list[PFF_Event], frames: list[PFF_Frame]) -> dict: ...


def add_carry_coordinates(events: list[PFF_Event], frames: list[PFF_Frame]) -> dict: ...
