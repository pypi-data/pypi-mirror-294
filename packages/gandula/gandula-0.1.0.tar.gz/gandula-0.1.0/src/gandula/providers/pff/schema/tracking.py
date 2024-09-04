from datetime import datetime
from enum import Enum

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import model_validator


class JerseyConfidence(Enum):
    HIGH = 'HIGH'
    MEDIUM = 'MEDIUM'
    LOW = 'LOW'


class Visibility(Enum):
    VISIBLE = 'VISIBLE'
    ESTIMATED = 'ESTIMATED'


class Player(BaseModel):
    jersey: int = Field(alias='jerseyNum')
    jersey_confidence: JerseyConfidence = Field(alias='confidence')
    visibility: Visibility
    x: float
    y: float


class Ball(BaseModel):
    visibility: Visibility
    x: float | None
    y: float | None
    z: float | None


class GameEventType(Enum):
    FIRST_KICK_OFF = 'FIRSTKICKOFF'
    SECOND_KICK_OFF = 'SECONDKICKOFF'
    THIRD_KICK_OFF = 'THIRDKICKOFF'
    FOURTH_KICK_OFF = 'FOURTHKICKOFF'
    FIRST_HALF_KICKOFF = '1KO'
    SECOND_HALF_KICKOFF = '2KO'
    END_OF_HALF = 'END'
    PBC_IN_PLAY = 'G'
    PLAYER_ON = 'ON'
    PLAYER_OFF = 'OFF'
    ON_THE_BALL = 'OTB'
    OUT_OF_PLAY = 'OUT'
    SUB = 'SUB'
    VIDEO_MISSING = 'VID'
    CLOCK = 'CLK'  # TODO: Check if this is correct


class SetPieceType(Enum):
    CORNER = 'C'
    DROP_BALL = 'D'
    FREE_KICK = 'F'
    GOAL_KICK = 'G'
    KICK_OFF = 'K'
    PENALTY = 'P'
    THROW_IN = 'T'


class Event(BaseModel):
    game_id: int
    game_event_type: GameEventType
    competition_id: int | None = None
    season: str | int | None = None
    clock: str | None = Field(alias='formatted_game_clock')
    player_id: int | None
    team_id: int | None
    setpiece_type: SetPieceType | None = None
    touches: int | None = Field(
        None, description='Number of touches taken by player on-the-ball'
    )
    touches_in_box: int | None = Field(
        None, description='Number of touches taken by player on-the-ball in the box'
    )
    start_time_seconds: float = Field(alias='start_time')
    end_time_seconds: float | None = Field(alias='end_time', default=None)
    duration_seconds: float | None = Field(alias='duration', default=None)
    video_missing: bool | None = Field(default=False)
    inserted_at: datetime
    updated_at: datetime
    start_frame: int = Field(description='The frame at which this GameEventType starts')
    end_frame: int | None = Field(
        None, description='The frame at which this GameEventType starts'
    )


class PossessionEventType(Enum):
    BALL_CARRY = 'BC'
    CHALLENGE = 'CH'  # includes dribbles
    CLEARANCE = 'CL'
    CROSS = 'CR'
    PASS = 'PA'
    REBOUND = 'RE'
    SHOT = 'SH'


class Possession(BaseModel):
    duration_seconds: float | None = Field(alias='duration', default=None)
    end_time_seconds: float | None = Field(alias='end_time', default=None)
    game_clock: str | None = Field(alias='formatted_game_clock')
    game_event_id: int
    game_id: int
    inserted_at: datetime
    possession_event_type: PossessionEventType
    start_time_seconds: float = Field(alias='start_time')
    updated_at: datetime
    start_frame: int
    end_frame: int | None = None


class PFF_Frame(BaseModel):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    away_players: list[Player] | None = Field(default_factory=list, alias='awayPlayers')
    away_players_with_kalman: list[Player] | None = Field(alias='awayPlayersSmoothed')
    ball: list[Ball] | None = Field(alias='balls')
    ball_with_kalman: Ball | None = Field(alias='ballsSmoothed')
    elapsed_seconds: float = Field(alias='periodElapsedTime')
    event: Event | None = Field(None, alias='game_event')
    event_id: int | None = Field(None, alias='game_event_id')
    frame_id: int = Field(alias='frameNum')
    game_clock_seconds: float = Field(alias='periodGameClockTime')
    game_ref_id: int | None = Field(None, alias='gameRefId')
    generated_time: datetime | None = Field(alias='generatedTime')
    home_ball: int | None = None
    home_players: list[Player] | None = Field(alias='homePlayers')
    home_players_with_kalman: list[Player] | None = Field(alias='homePlayersSmoothed')
    period: int = Field(alias='period')
    possession: Possession | None = Field(None, alias='possession_event')
    possession_id: int | None = Field(None, alias='possession_event_id')
    sequence: int | None = None
    version: str | None
    video_time_milli: float = Field(alias='videoTimeMs')

    def find_player_by_shirt(self, shirt: int, is_home: bool) -> Player:
        player_list = self.home_players if is_home else self.away_players
        if not player_list:
            raise ValueError(f'Frame {self.frame_id} has no players')
        return next(p for p in player_list if int(p.jersey) == shirt)

    def get_player_coordinates(self, shirt: int, is_home: bool) -> tuple[float, float]:
        try:
            player = self.find_player_by_shirt(shirt, is_home)
            return player.x, player.y
        except StopIteration:
            try:
                player = self.find_player_by_shirt(shirt, not is_home)
                return player.x, player.y
            except StopIteration as exc:
                raise StopIteration(
                    f'Player {shirt} not found in frame {self.frame_id}'
                ) from exc

    def __repr__(self):
        return f'Frame {self.frame_id} - {self.game_clock_seconds}'


# TODO: Rename class
class PFF_Frames(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, allow_none=True)

    frames: list[PFF_Frame] = Field(default_factory=list)
    game_id: int

    @model_validator(mode='after')
    def sort_frames(self):
        self.frames = sorted(self.frames, key=lambda f: f.frame_id)
        return self

    def get_frame(self, frame_id: int) -> PFF_Frame:
        return next(f for f in self.frames if f.frame_id == frame_id)

    def get_frames_with_event(self) -> dict[str, list[PFF_Frame]]:
        frames_with_events: dict[str, list[PFF_Frame]] = {}

        for frame in self.frames:
            if not frame.event_id:
                continue

            events_list = frames_with_events.get(str(frame.event_id), None)

            if not events_list:
                frames_with_events[str(frame.event_id)] = [frame]
            else:
                events_list.append(frame)

        return frames_with_events

    def get_frames_with_possession(self) -> list[PFF_Frame]:
        return [f for f in self.frames if f.possession_id]

    def get_frame_by_event(self, event_id: int) -> list[PFF_Frame]:
        return [f for f in self.frames if f.event_id == event_id]

    def get_frame_by_possession_id(self, possession_id: int) -> PFF_Frame:
        return next(f for f in self.frames if f.possession_id == possession_id)

    def get_frame_by_event_type(self, event_type: GameEventType) -> list[PFF_Frame]:
        return [
            f for f in self.frames if f.event and f.event.game_event_type == event_type
        ]

    def get_frame_by_possession_type(
        self, possession_event_type: PossessionEventType
    ) -> list[PFF_Frame]:
        return [
            f
            for f in self.frames
            if f.possession
            and f.possession.possession_event_type == possession_event_type
        ]

    def get_frame_in_range(self, start_frame: int, end_frame: int) -> list[PFF_Frame]:
        return [f for f in self.frames if start_frame <= f.frame_id <= end_frame]

    def get_frame_by_sequence(self, sequence_id: int) -> list[PFF_Frame]:
        return [f for f in self.frames if f.sequence == sequence_id]

    # TODO: add functionality to extract from frames:
    # distance run, speed, accel, max_speed, max_accel, avg_pos, longest_run_with_ball
    # minutes played, heatmap-ready objs, etc.
    # Report data is necessary because not all tracks will have full event data support
