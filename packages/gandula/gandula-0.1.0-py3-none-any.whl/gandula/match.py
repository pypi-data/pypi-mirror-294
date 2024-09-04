import ast
from pathlib import Path

from gandula.enhance_events import add_pass_coordinates
from gandula.enhance_events import add_shot_coordinates
from gandula.providers.pff.api import match
from gandula.providers.pff.local import loader as local_loader
from gandula.providers.pff.schema.event import PFF_Event
from gandula.providers.pff.schema.event import PFF_Game
from gandula.providers.pff.schema.event import Roster
from gandula.providers.pff.schema.tracking import PFF_Frame


def get_match_events(
    match_id: int, *, api_url: str | None = None, api_key: str | None = None
) -> list[PFF_Event]:
    try:
        events = match.get_match_events(
            match_id, pff_api_url=api_url, pff_api_key=api_key
        )
        return [PFF_Event.model_validate(event) for event in events['gameEvents']]
    except Exception as exc:
        raise Exception(f'Error getting match events for match_id={match_id}') from exc


def get_match(
    match_id: int,
    *,
    api_url: str | None = None,
    api_key: str | None = None,
    events_path: str | None = None,
) -> PFF_Game:
    try:
        if events_path is None:
            pff_match = match.get_match(
                match_id, pff_api_url=api_url, pff_api_key=api_key
            )
        else:
            pff_events = local_loader.read_json(Path(events_path) / 'events.json')
            pff_events = [
                PFF_Event.model_validate(event)
                for event in pff_events
                if event['gameId'] == int(match_id)
            ]

            pff_roosters = local_loader.read_csv(Path(events_path) / 'rosters.csv')
            pff_roosters.rename(columns={'game_id': 'gameId'}, inplace=True)
            pff_roosters = pff_roosters[pff_roosters['gameId'] == int(match_id)]
            pff_roosters['player'] = pff_roosters['player'].apply(ast.literal_eval)
            pff_roosters['team'] = pff_roosters['team'].apply(ast.literal_eval)
            pff_roosters = pff_roosters.to_dict(orient='records')
            pff_roosters = [Roster.model_validate(roster) for roster in pff_roosters]

            pff_metadata = local_loader.read_csv(Path(events_path) / 'metadata.csv')
            pff_metadata = pff_metadata[pff_metadata['id'] == int(match_id)]
            columns_to_convert = [
                'awayTeam',
                'awayTeamKit',
                'competition',
                'homeTeam',
                'homeTeamKit',
                'stadium',
                'videos',
            ]
            for col in columns_to_convert:
                pff_metadata[col] = pff_metadata[col].apply(ast.literal_eval)
            pff_metadata = pff_metadata.to_dict(orient='records')[0]

            pff_match = {'game': pff_metadata}
            pff_match['game']['gameEvents'] = pff_events
            pff_match['game']['rosters'] = pff_roosters

        return PFF_Game.model_validate(pff_match['game'])
    except Exception as exc:
        raise Exception(f'Error getting match for match_id={match_id}') from exc


def get_match_event(
    event_id: int, *, api_url: str | None = None, api_key: str | None = None
) -> PFF_Event:
    try:
        event = match.get_match_event(
            event_id, pff_api_url=api_url, pff_api_key=api_key
        )
        return PFF_Event.model_validate(**event)
    except Exception as exc:
        raise Exception(f'Error getting match event for event_id={event_id}') from exc


def get_frames(
    data_dir: str,
    match_id: int,
    *,
    competition_name: str | None = None,
    season: str | None = None,
) -> list[PFF_Frame]:
    try:
        frames = local_loader.get_frames(
            data_dir, match_id, competition_name=competition_name, season=season
        )
        return [PFF_Frame.model_validate(frame, strict=False) for frame in frames]
    except Exception as exc:
        raise Exception(f'Error getting frames for match_id={match_id}') from exc


def get_enhanced_frames(
    data_dir: str,
    match_id: int,
    *,
    competition_name: str | None = None,
    season: str | None = None,
    events_path: str | None = None,
):
    pff_match = get_match(match_id, events_path=events_path)
    frames = get_frames(
        data_dir, match_id, competition_name=competition_name, season=season
    )

    passes = add_pass_coordinates(pff_match, frames)
    shots = add_shot_coordinates(pff_match, frames)

    enhanced_frames = []

    for frame in frames:
        frame_id_str = str(frame.frame_id)
        if passes.get(frame_id_str):
            enhanced_frames.append(passes[frame_id_str])
        elif shots.get(frame_id_str):
            enhanced_frames.append(shots[frame_id_str])
        else:
            enhanced_frames.append({'frame': frame, 'event': None})

    return enhanced_frames
