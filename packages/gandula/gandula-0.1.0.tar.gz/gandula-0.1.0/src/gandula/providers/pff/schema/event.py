from __future__ import annotations

from enum import Enum

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class BallCarryType(str, Enum):
    CARRY = 'C'
    DRIBBLE = 'D'
    TOUCH = 'T'


class BetterOptionType(str, Enum):
    BALL_CARRY = 'B'
    CROSS = 'C'
    HOLD = 'H'
    CLEARANCE = 'L'
    CONTINUE = 'O'
    PASS = 'P'
    SHOT = 'S'


class BodyMovementType(str, Enum):
    AWAY_FROM_GOAL = 'AG'
    LATERALLY = 'LA'
    STATIC = 'ST'
    TOWARDS_GOAL = 'TG'


class BodyType(str, Enum):
    BACK = 'BA'
    BOTTOM = 'BO'
    TWO_HAND_CATCH = 'CA'
    CHEST = 'CH'
    HEAD = 'HE'
    LEFT_FOOT = 'L'
    LEFT_ARM = 'LA'
    LEFT_BACK_HEEL = 'LB'
    LEFT_SHOULDER = 'LC'
    LEFT_HAND = 'LH'
    LEFT_KNEE = 'LK'
    LEFT_SHIN = 'LS'
    LEFT_THIGH = 'LT'
    TWO_HAND_PALM = 'PA'
    TWO_HAND_PUNCH = 'PU'
    RIGHT_FOOT = 'R'
    RIGHT_ARM = 'RA'
    RIGHT_BACK_HEEL = 'RB'
    RIGHT_SHOULDER = 'RC'
    RIGHT_HAND = 'RH'
    RIGHT_KNEE = 'RK'
    RIGHT_SHIN = 'RS'
    RIGHT_THIGH = 'RT'
    TWO_HANDS = 'TWOHANDS'
    VIDEO_MISSING = 'VM'


class CarryType(str, Enum):
    LINE_BREAK = 'B'
    CHANGE_OF_DIRECTION = 'C'
    DRIVE_WITH_INTENT = 'D'
    LONG_CARRY = 'L'


class ChallengeOutcomeType(str, Enum):
    DISTRIBUTION_DISRUPTED = 'B'
    FORCED_OUT_OF_PLAY = 'C'
    DISTRIBUTES_BALL = 'D'
    FOUL = 'F'
    SHIELDS_IN_PLAY = 'I'
    KEEPS_BALL_WITH_CONTACT = 'K'
    ROLLS = 'L'
    BEATS_MAN_LOSES_BALL = 'M'
    NO_WIN_KEEP_BALL = 'N'
    OUT_OF_PLAY = 'O'
    PLAYER = 'P'
    RETAIN = 'R'
    SHIELDS_OUT_OF_PLAY = 'S'


class ChallengeType(str, Enum):
    AERIAL_DUEL = 'A'
    FROM_BEHIND = 'B'
    DRIBBLE = 'D'
    FIFTY = 'FIFTY'
    GK_SMOTHERS = 'G'
    SHIELDING = 'H'
    HAND_TACKLE = 'K'
    SLIDE_TACKLE = 'L'
    SHOULDER_TO_SHOULDER = 'S'
    STANDING_TACKLE = 'T'


class ClearanceOutcomeType(str, Enum):
    LUCKY_SHOT_AT_GOAL = 'A'
    BLOCK = 'B'
    LUCKY_SHOT_OWN_GOAL = 'D'
    OWN_POST = 'N'
    OUT_OF_PLAY = 'O'
    PLAYER = 'P'
    STOPPAGE = 'S'
    POST = 'W'


class CrossOutcomeType(str, Enum):
    BLOCKED = 'B'
    COMPLETE = 'C'
    DEFENSIVE_INTERCEPTION = 'D'
    LUCKY_SHOT_AT_GOAL = 'I'
    OUT_OF_PLAY = 'O'
    STOPPAGE = 'S'
    UNTOUCHED = 'U'


class CrossType(str, Enum):
    DRILLED = 'D'
    FLOATED = 'F'
    SWING_IN = 'I'
    SWING_OUT = 'O'
    PLACED = 'P'


class CrossZoneType(str, Enum):
    CENTRAL = 'C'
    FAR_POST = 'F'
    NEAR_POST = 'N'
    SIX_YARD_BOX = 'S'


class DribbleOutcomeType(str, Enum):
    KEEPS_BALL_WITH_CONTACT = 'B'
    FOUL = 'F'
    MISHIT = 'H'
    KEEPS_BALL = 'K'
    BEATS_MAN_LOSES_BALL = 'L'
    MISSED_FOUL = 'M'
    FORCED_OUT_OF_PLAY = 'O'
    SUCCESSFUL_TACKLE = 'S'


class DribbleType(str, Enum):
    BETWEEN_TWO_DEFENDERS = 'B'
    INSIDE = 'I'
    KNOCKS_IN_FRONT = 'K'
    OUTSIDE = 'O'
    TRICK = 'T'


class EndType(str, Enum):
    EXTRA_1 = 'F'
    FIRST = 'FIRST'
    GAME = 'G'
    EXTRA_2 = 'S'
    SECOND = 'SECOND'
    Z_TEST_9 = 'Z'


class FacingType(str, Enum):
    BACK_TO_GOAL = 'B'
    GOAL = 'G'
    LATERAL = 'L'


class FoulOutcomeType(str, Enum):
    NO_FOUL = 'F'
    NO_WARNING = 'N'
    RED_CARD = 'R'
    SECOND_YELLOW = 'S'
    WARNING = 'W'
    YELLOW_CARD = 'Y'


class FoulType(str, Enum):
    ADVANTAGE = 'A'
    INFRINGEMENT = 'I'
    MISSED_INFRINGEMENT = 'M'


class PFF_EventType(str, Enum):
    GAME_CLOCK_OBSERVATION = 'CLK'
    END_OF_HALF = 'END'
    FIRST_HALF_KICKOFF = 'FIRSTKICKOFF'
    EXTRA_2_KICKOFF = 'FOURTHKICKOFF'
    GROUND = 'G'
    PLAYER_OFF = 'OFF'
    PLAYER_ON = 'ON'
    POSSESSION = 'OTB'
    BALL_OUT_OF_PLAY = 'OUT'
    PAUSE_OF_GAME_TIME = 'PAU'
    SECOND_HALF_KICKOFF = 'SECONDKICKOFF'
    SUB = 'SUB'
    EXTRA_1_KICKOFF = 'THIRDKICKOFF'
    VIDEO = 'VID'


class HeightType(str, Enum):
    ABOVE_HEAD = 'A'
    GROUND = 'G'
    BETWEEN_WAIST_AND_HEAD = 'H'
    OFF_GROUND_BELOW_WAIST = 'L'
    VIDEO_MISSING = 'M'
    HALF_VOLLEY = 'V'


class IncompletionReasonType(str, Enum):
    BEHIND = 'BH'
    BLOCKED = 'BL'
    CAUGHT = 'CA'
    DEFENSIVE_CONTACT = 'CO'
    DELIBERATE = 'DB'
    DEFENSIVE_CHALLENGE = 'DC'
    DEFLECTED = 'DF'
    DEFENDER_INTERCEPTION = 'DI'
    FOUL = 'FO'
    HIGH = 'HI'
    HIT_OFFICIAL = 'HO'
    IN_FRONT = 'IF'
    RECEIVER_LETS_BALL_RUN = 'LB'
    MISCOMMUNICATION = 'MC'
    MISS_HIT = 'MH'
    PASSER_SLIPPED = 'PS'
    RECEIVER_DIDNT_RETURN_TO_BALL = 'RB'
    RECEIVER_SLIPPED = 'RF'
    RECEIVER_MISSES_BALL = 'RM'
    RECEIVER_STOPPED = 'RS'
    REFEREE_IN_WAY = 'RW'
    SPECULATIVE = 'SP'
    UNDERHIT = 'UH'


class InitialTouchType(str, Enum):
    H2C_BAD = 'B'
    H2C_GOOD = 'G'
    MISCONTROL = 'M'
    STANDARD = 'S'


class LinesBrokenType(str, Enum):
    ATT = 'A'
    ATT_MID = 'AM'
    ATT_MID_DEF = 'AMD'
    DEF = 'D'
    MID = 'M'
    MID_DEF = 'MD'


class MissedTouchType(str, Enum):
    DUMMY = 'D'
    MISSED_TOUCH = 'M'
    SLIP = 'S'


class OpportunityType(str, Enum):
    CHANCE_CREATED = 'C'
    DANGEROUS_POSITION = 'D'
    HALF_CHANCE = 'H'
    SPACE_TO_CLEAR = 'L'
    NEGATIVE_CHANCE_CREATED = 'N'
    NEGATIVE_DANGEROUS_POSITION = 'P'
    SPACE_TO_CROSS = 'R'
    SPACE_TO_SHOOT = 'S'


class OriginateType(str, Enum):
    CORNER_FLAG = 'C'
    MISCELLANEOUS = 'M'
    PLAYER = 'P'
    POST = 'W'


class OutType(str, Enum):
    AWAY_SCORE = 'A'
    HOME_SCORE = 'H'
    TOUCH = 'T'
    WHISTLE = 'W'


class PassAccuracyType(str, Enum):
    CHECKS_MOVEMENT = 'C'
    HEAVY = 'H'
    LIGHT = 'L'
    PRECISE = 'P'
    REDIRECTS = 'R'
    STANDARD = 'S'


class PassOutcomeType(str, Enum):
    BLOCKED = 'B'
    COMPLETE = 'C'
    DEFENSIVE_INTERCEPTION = 'D'
    LUCKY_SHOT_OWN_GOAL = 'G'
    LUCKY_SHOT_GOAL = 'I'
    OUT_OF_PLAY = 'O'
    STOPPAGE = 'S'


class PassType(str, Enum):
    CUTBACK = 'B'
    CREATE_CONTEST = 'C'
    FLICK_ON = 'F'
    LONG_PASS = 'L'
    MISS_HIT = 'M'
    BALL_OVER_THE_TOP = 'O'
    STANDARD_PASS = 'S'
    THROUGH_BALL = 'T'


class PlayerOffType(str, Enum):
    INJURY = 'I'
    RED_CARD = 'R'
    YELLOW_CARD = 'Y'


class PositionGroupType(str, Enum):
    ATTACK_MID = 'AM'
    CENTER_FORWARD = 'CF'
    CENTER_MID = 'CM'
    DEFENDER = 'D'
    DEFENSIVE_MID = 'DM'
    FORWARD = 'F'
    GK = 'GK'
    LEFT_BACK = 'LB'
    LEFT_CENTER_BACK = 'LCB'
    LEFT_MID = 'LM'
    LEFT_WINGER = 'LW'
    LEFT_WING_BACK = 'LWB'
    MIDFIELDER = 'M'
    MID_CENTER_BACK = 'MCB'
    RIGHT_BACK = 'RB'
    RIGHT_CENTER_BACK = 'RCB'
    CENTER_BACK = 'CB'
    RIGHT_MID = 'RM'
    RIGHT_WINGER = 'RW'
    RIGHT_WING_BACK = 'RWB'


class PFF_PossessionEventType(str, Enum):
    BALL_CARRY = 'BC'
    CHALLENGE = 'CH'
    CLEARANCE = 'CL'
    CROSS = 'CR'
    PASS = 'PA'
    REBOUND = 'RE'
    SHOT = 'SH'


class PotentialOffenseType(str, Enum):
    DISSENT = 'D'
    OFF_THE_BALL = 'F'
    HAND_BALL = 'H'
    ON_THE_BALL = 'N'
    OFFSIDE = 'O'
    TECHNICAL = 'T'
    DIVA = 'V'


class PressureType(str, Enum):
    ATTEMPTED = 'A'
    PASSING_LANE = 'L'
    PRESSURED = 'P'


class ReboundOutcomeType(str, Enum):
    LUCKY_SHOT_GOAL = 'A'
    LUCKY_SHOT_OWN_GOAL = 'D'
    PLAYER = 'P'
    RETAIN = 'R'
    OUT_OF_TOUCH = 'T'


class SaveReboundType(str, Enum):
    CROSSBAR = 'CB'
    LEFT_BEHIND_GOAL = 'GL'
    RIGHT_BEHIND_GOAL = 'GR'
    LEFT_BEHIND_GOAL_HIGH = 'HL'
    RIGHT_BEHIND_GOAL_HIGH = 'HR'
    LEFT_SIX_YARD_BOX = 'L6'
    LEFT_AREA = 'LA'
    LEFT_OUT_OF_BOX = 'LO'
    LEFT_POST = 'LP'
    MIDDLE_SIX_YARD_BOX = 'M6'
    MIDDLE_AREA = 'MA'
    MIDDLE_OUT_OF_BOX = 'MO'
    CROSSBAR_OVER = 'OC'
    RIGHT_SIX_YARD_BOX = 'R6'
    RIGHT_AREA = 'RA'
    RIGHT_OUT_OF_BOX = 'RO'
    RIGHT_POST = 'RP'


class SetpieceType(str, Enum):
    CORNER = 'C'
    DROP_BALL = 'D'
    FREE_KICK = 'F'
    GOAL_KICK = 'G'
    KICKOFF = 'K'
    PENALTY = 'P'
    THROW_IN = 'T'


class ShotHeightType(str, Enum):
    BOTTOM_THIRD = 'BOTTOMTHIRD'
    CROSSBAR = 'C'
    SHORT = 'F'
    GROUND = 'G'
    MIDDLE_THIRD = 'MIDDLETHIRD'
    CROSSBAR_NARROW_OVER = 'N'
    OVER = 'O'
    TOP_THIRD = 'TOPTHIRD'
    CROSSBAR_NARROW_UNDER = 'U'


class ShotNatureType(str, Enum):
    PLACEMENT = 'A'
    FLICK = 'F'
    LACES = 'L'
    POWER = 'P'
    SCUFF = 'S'
    TOE_PUNT = 'T'


class ShotOutcomeType(str, Enum):
    ON_TARGET_BLOCK = 'B'
    OFF_TARGET_BLOCK = 'C'
    SAVE_OFF_TARGET = 'F'
    GOAL = 'G'
    GOALLINE_CLEARANCE = 'L'
    OFF_TARGET = 'O'
    ON_TARGET = 'S'


class ShotType(str, Enum):
    BICYCLE = 'B'
    DIVING = 'D'
    SIDE_FOOT = 'F'
    SLIDING = 'I'
    LOB = 'L'
    OUTSIDE_FOOT = 'O'
    STANDARD = 'S'
    STUDS = 'T'
    VOLLEY = 'V'


class StadiumGrassType(str, Enum):
    ASTRO_TURF = 'A'
    FIELD_TURF = 'F'
    REAL = 'R'


class StadiumType(str, Enum):
    CONVERSION = 'C'
    DOMED = 'D'
    INDOOR = 'I'
    OUTDOOR = 'O'


class SubType(str, Enum):
    BLOOD = 'B'
    SIN_BIN_COVER = 'C'
    HEAD = 'H'
    RETURN_FROM_HIA = 'R'
    STANDARD = 'S'


class TackleAttemptType(str, Enum):
    DELIBERATE_FOUL = 'D'
    NO_TACKLE_FAKE_EVENT = 'F'
    GO_FOR_BALL = 'G'
    NO_TACKLE = 'T'


class TouchOutcomeType(str, Enum):
    CHALLENGE = 'C'
    GOAL = 'G'
    OUT_OF_PLAY = 'O'
    PLAYER = 'P'
    OWN_GOAL = 'W'


class TouchType(str, Enum):
    BALL_IN_HAND = 'B'
    FAILED_CROSS = 'C'
    HAND_BALL = 'D'
    FAILED_TRAP = 'F'
    FAILED_CATCH = 'G'
    HEAVY_TOUCH = 'H'
    FAILED_CLEARANCE = 'L'
    FAILED_PASS = 'P'
    FAILED_SHOT = 'S'
    TAKE_OVER = 'T'


class VarReasonType(str, Enum):
    MISSED = 'I'
    OVERTURN = 'O'


class VideoAngleType(str, Enum):
    BAD_ANGLE = 'B'
    MISSING = 'M'


class _ID(BaseModel):
    id: str | None = None


class BallCarryEvent(BaseModel):
    id: str | None = None
    additionalChallenger1: Player | None = None
    additionalChallenger2: Player | None = None
    additionalChallenger3: Player | None = None
    ballCarrierPlayer: Player | None = None
    ballCarryEndPointX: float | None = None
    ballCarryEndPointY: float | None = None
    ballCarryStartPointX: float | None = None
    ballCarryStartPointY: float | None = None
    ballCarryType: BallCarryType | None = None
    carryType: CarryType | None = None
    challengerPlayer: Player | None = None
    createsSpace: bool | None = None
    defenderPlayer: Player | None = None
    defenderPointX: float | None = None
    defenderPointY: float | None = None
    dribbleEndPointX: float | None = None
    dribbleEndPointY: float | None = None
    dribbleOutcomeType: DribbleOutcomeType | None = None
    dribbleStartPointX: float | None = None
    dribbleStartPointY: float | None = None
    dribbleType: DribbleType | None = None
    game: PFF_Game | None = None
    gameEvent: PFF_Event | None = None
    linesBrokenType: LinesBrokenType | None = None
    opportunityType: OpportunityType | None = None
    period: str | int | None = None
    possessionEvent: PFF_PossessionEvent | None = None
    pressurePlayer: Player | None = None
    tackleAttemptPointX: float | None = None
    tackleAttemptPointY: float | None = None
    tackleAttemptType: TackleAttemptType | None = None
    touchOutcomePlayer: Player | None = None
    touchOutcomeType: TouchOutcomeType | None = None
    touchPointX: float | None = None
    touchPointY: float | None = None
    touchType: TouchType | None = None
    trickType: str | None = None


class CacheStats(BaseModel):
    hitRate: float | None = None
    name: str | None = None


class ChallengeEvent(BaseModel):
    id: str | None = None
    additionalChallenger1: Player | None = None
    additionalChallenger2: Player | None = None
    additionalChallenger3: Player | None = None
    ballCarrierPlayer: Player | None = None
    challengeOutcomeType: ChallengeOutcomeType | None = None
    challengePointX: float | None = None
    challengePointY: float | None = None
    challengeType: ChallengeType | None = None
    challengeWinnerPlayer: Player | None = None
    challengerAwayPlayer: Player | None = None
    challengerHomePlayer: Player | None = None
    challengerPlayer: Player | None = None
    createsSpace: bool | None = None
    dribbleEndPointX: float | None = None
    dribbleEndPointY: float | None = None
    dribbleStartPointX: float | None = None
    dribbleStartPointY: float | None = None
    dribbleType: DribbleType | None = None
    game: PFF_Game | None = None
    gameEvent: PFF_Event | None = None
    keeperPlayer: Player | None = None
    linesBrokenType: LinesBrokenType | None = None
    opportunityType: OpportunityType | None = None
    period: str | None = None
    possessionEvent: PFF_PossessionEvent | None = None
    pressurePlayer: Player | None = None
    tackleAttemptPointX: float | None = None
    tackleAttemptPointY: float | None = None
    tackleAttemptType: TackleAttemptType | None = None
    trickType: str | None = None


class ClearanceEvent(BaseModel):
    ballHeightType: str | None = None
    ballHighPointType: str | None = None
    blockerPlayer: Player | None = None
    clearanceBodyType: BodyType | None = None
    clearanceEndPointX: float | None = None
    clearanceEndPointY: float | None = None
    clearanceOutcomeType: ClearanceOutcomeType | None = None
    clearancePlayer: Player | None = None
    clearancePointX: float | None = None
    clearancePointY: float | None = None
    clearanceStartPointX: float | None = None
    clearanceStartPointY: float | None = None
    createsSpace: bool | None = None
    defenderPlayer: Player | None = None
    failedInterventionPlayer: Player | None = None
    failedInterventionPlayer1: Player | None = None
    failedInterventionPlayer2: Player | None = None
    failedInterventionPlayer3: Player | None = None
    game: PFF_Game | None = None
    gameEvent: PFF_Event | None = None
    id: str | None = None
    keeperPlayer: Player | None = None
    opportunityType: OpportunityType | None = None
    period: str | None = None
    possessionEvent: PFF_PossessionEvent | None = None
    pressurePlayer: Player | None = None
    pressureType: PressureType | None = None
    shotInitialHeightType: ShotHeightType | None = None
    shotOutcomeType: ShotOutcomeType | None = None


class Competition(BaseModel):
    availableSeasons: list[CompetitionSeason] | None = Field(default_factory=list)
    id: str | None = None
    games: list[PFF_Game] | None = Field(default_factory=list)
    name: str | None = None
    seasonGames: list[PFF_Game] | None = Field(default_factory=list)
    teams: list[Team] | None = Field(default_factory=list)


class CompetitionSeason(BaseModel):
    season: str | None = None
    start: str | None = None
    end: str | None = None


class Confederation(BaseModel):
    id: str | None = None
    abbreviation: str | None = None
    name: str | None = None


class CrossEvent(BaseModel):
    ballHeightType: HeightType | None = None
    blockerPlayer: Player | None = None
    clearerPlayer: Player | None = None
    completeToPlayer: Player | None = None
    createsSpace: bool | None = None
    crossEndPointX: float | None = None
    crossEndPointY: float | None = None
    crossHighPointType: str | None = None
    crossOutcomeType: CrossOutcomeType | None = None
    crossPointX: float | None = None
    crossPointY: float | None = None
    crossStartPointX: float | None = None
    crossStartPointY: float | None = None
    crossType: CrossType | None = None
    crossZoneType: CrossZoneType | None = None
    crosserBodyType: BodyType | None = None
    crosserPlayer: Player | None = None
    defenderBallHeightType: HeightType | None = None
    defenderBodyType: BodyType | None = None
    defenderPlayer: Player | None = None
    deflectionPointX: float | None = None
    deflectionPointY: float | None = None
    deflectorBodyType: BodyType | None = None
    deflectorPlayer: Player | None = None
    failedInterventionPlayer: Player | None = None
    failedInterventionPlayer1: Player | None = None
    failedInterventionPlayer2: Player | None = None
    failedInterventionPlayer3: Player | None = None
    failedInterventionPointX: float | None = None
    failedInterventionPointY: float | None = None
    game: PFF_Game | None = None
    gameEvent: PFF_Event | None = None
    goalkeeperPointX: float | None = None
    goalkeeperPointY: float | None = None
    id: str | None = None
    incompletionReasonType: IncompletionReasonType | None = None
    intendedTargetPlayer: Player | None = None
    intendedTargetPointX: float | None = None
    intendedTargetPointY: float | None = None
    keeperPlayer: Player | None = None
    linesBrokenType: LinesBrokenType | None = None
    opportunityType: OpportunityType | None = None
    period: str | None = None
    possessionEvent: PFF_PossessionEvent | None = None
    pressurePlayer: Player | None = None
    pressureType: PressureType | None = None
    receiverBallHeightType: HeightType | None = None
    receiverBodyType: BodyType | None = None
    receiverPointX: float | None = None
    receiverPointY: float | None = None
    secondIncompletionReasonType: IncompletionReasonType | None = None
    shotInitialHeightType: ShotHeightType | None = None
    shotOutcomeType: ShotOutcomeType | None = None
    targetZonePointX: float | None = None
    targetZonePointY: float | None = None


class Defender(BaseModel):
    id: str | None = None
    defenderPlayer: Player | None = None
    defenderPointX: float | None = None
    defenderPointY: float | None = None
    game: PFF_Game | None = None
    gameEvent: PFF_Event | None = None
    possessionEvent: PFF_PossessionEvent | None = None


class Federation(BaseModel):
    id: str | None = None
    name: str | None = None
    englishName: str | None = None
    abbreviation: str | None = None
    confederation: Confederation | None = None
    country: str | None = None


class Foul(BaseModel):
    id: str | None = None
    badCall: bool | None = None
    correctDecision: bool | None = None
    culpritPlayer: Player | None = None
    foulOutcomeType: FoulOutcomeType | None = None
    foulPointX: float | None = None
    foulPointY: float | None = None
    foulType: FoulType | None = None
    game: PFF_Game | None = None
    gameEvent: PFF_Event | None = None
    possessionEvent: PFF_PossessionEvent | None = None
    potentialOffenseType: PotentialOffenseType | None = None
    sequence: int | None = None
    tacticalFoul: bool | None = None
    var: bool | None = None
    varCulpritPlayer: Player | None = None
    varOutcomeType: FoulOutcomeType | None = None
    varPotentialOffenseType: PotentialOffenseType | None = None
    varReasonType: VarReasonType | None = None
    victimPlayer: Player | None = None


class Location(BaseModel):
    id: str | None = None
    ballCarryEvent: BallCarryEvent | None = None
    challengeEvent: ChallengeEvent | None = None
    clearanceEvent: ClearanceEvent | None = None
    crossEvent: CrossEvent | None = None
    gameEvent: PFF_Event | None = None
    name: str | None = None
    passingEvent: PassingEvent | None = None
    possessionEvent: PFF_PossessionEvent | None = None
    reboundEvent: ReboundEvent | None = None
    shootingEvent: ShootingEvent | None = None
    x: float | None = None
    y: float | None = None


class Nation(BaseModel):
    country: str | None = None
    federation: Federation | None = None
    fifaCode: str | None = None
    id: str | None = None
    iocCode: str | None = None


class PassingEvent(BaseModel):
    ballHeightType: HeightType | None = None
    blockerPlayer: Player | None = None
    clearerPlayer: Player | None = None
    defenderBodyType: BodyType | None = None
    defenderHeightType: HeightType | None = None
    defenderPlayer: Player | None = None
    defenderPointX: float | None = None
    defenderPointY: float | None = None
    deflectionPointX: float | None = None
    deflectionPointY: float | None = None
    deflectorBodyType: BodyType | None = None
    deflectorPlayer: Player | None = None
    failedInterventionPlayer: Player | None = None
    failedInterventionPlayer1: Player | None = None
    failedInterventionPlayer2: Player | None = None
    failedInterventionPlayer3: Player | None = None
    failedInterventionPointX: float | None = None
    failedInterventionPointY: float | None = None
    game: PFF_Game | None = None
    gameEvent: PFF_Event | None = None
    goalkeeperPointX: float | None = None
    goalkeeperPointY: float | None = None
    id: str | None = None
    incompletionReasonType: IncompletionReasonType | None = None
    keeperPlayer: Player | None = None
    linesBrokenType: LinesBrokenType | None = None
    missedTouchPlayer: Player | None = None
    missedTouchPointX: float | None = None
    missedTouchPointY: float | None = None
    missedTouchType: MissedTouchType | None = None
    onTarget: bool | None = None
    opportunityType: OpportunityType | None = None
    outOfPlayPointX: float | None = None
    outOfPlayPointY: float | None = None
    passAccuracyType: PassAccuracyType | None = None
    passBodyType: BodyType | None = None
    passHighPointType: HeightType | None = None
    passOutcomeType: PassOutcomeType | None = None
    passPointX: float | None = None
    passPointY: float | None = None
    passType: PassType | None = None
    passerPlayer: Player | None = None
    period: str | None = None
    possessionEvent: PFF_PossessionEvent | None = None
    pressurePlayer: Player | None = None
    pressureType: PressureType | None = None
    receiverBodyType: BodyType | None = None
    receiverFacingType: FacingType | None = None
    receiverHeightType: HeightType | None = None
    receiverPlayer: Player | None = None
    receiverPointX: float | None = None
    receiverPointY: float | None = None
    secondIncompletionReasonType: IncompletionReasonType | None = None
    shotInitialHeightType: ShotHeightType | None = None
    shotOutcomeType: ShotOutcomeType | None = None
    targetFacingType: FacingType | None = None
    targetPlayer: Player | None = None
    targetPointX: float | None = None
    targetPointY: float | None = None


class Player(BaseModel):
    id: str | None = None
    dob: str | None = None
    firstName: str | None = None
    gender: str | None = None
    height: float | None = None  # in cm
    lastName: str | None = None
    nickname: str | None = None
    preferredFoot: str | None = None
    weight: float | None = None
    positionGroupType: PositionGroupType | None = None
    nationality: Nation | None = None
    secondNationality: Nation | None = None
    countryOfBirth: Nation | None = None
    rosters: list[Roster] | None = Field(default_factory=list)


class PFF_PossessionEvent(BaseModel):
    id: str | None = None
    ballCarryEvent: BallCarryEvent | None = None
    challengeEvent: ChallengeEvent | None = None
    clearanceEvent: ClearanceEvent | None = None
    crossEvent: CrossEvent | None = None
    defenders: list[Defender] | None = Field(default_factory=list)
    duration: float | None = None
    endTime: float | None = None
    formattedGameClock: str | None = None
    fouls: list[Foul] | None = Field(default_factory=list)
    game: PFF_Game | None = None
    gameClock: float | None = None
    gameEvent: PFF_Event | None = None
    lastInGameEvent: int | None = None
    passingEvent: PassingEvent | None = None
    period: str | None = None
    possessionEventType: PFF_PossessionEventType | None = None
    reboundEvent: ReboundEvent | None = None
    shootingEvent: ShootingEvent | None = None
    startTime: float | None = None
    videoUrl: str | None = Field(default=None, exclude=True)

    def __repr__(self) -> str:
        return f'{self.possessionEventType}={self.id}'


class ReboundEvent(BaseModel):
    id: str | None = None
    game: PFF_Game | None = None
    gameEvent: PFF_Event | None = None
    period: str | None = None
    possessionEvent: PFF_PossessionEvent | None = None
    reboundBodyType: BodyType | None = None
    reboundEndPointX: float | None = None
    reboundEndPointY: float | None = None
    reboundHeightType: HeightType | None = None
    reboundHighPointType: HeightType | None = None
    reboundOutcomeType: ReboundOutcomeType | None = None
    reboundPointX: float | None = None
    reboundPointY: float | None = None
    reboundStartPointX: float | None = None
    reboundStartPointY: float | None = None
    rebounderPlayer: Player | None = None
    shotInitialHeightType: ShotHeightType | None = None
    shotOutcomeType: ShotOutcomeType | None = None


class Roster(BaseModel):
    id: str | None = None
    game: PFF_Game | None = None
    player: Player | None = None
    positionGroupType: PositionGroupType | None = None
    shirtNumber: str | int | None = None
    started: bool | None = None
    team: Team | None = None


class ShootingEvent(BaseModel):
    blockerPlayer: Player | None = None
    clearerPlayer: Player | None = None
    createsSpace: bool | None = None
    deflectionPointX: float | None = None
    deflectionPointY: float | None = None
    deflectorBodyType: BodyType | None = None
    deflectorPlayer: Player | None = None
    goalLineEndPointX: float | None = None
    goalLineEndPointY: float | None = None
    goalLineStartPointX: float | None = None
    goalLineStartPointY: float | None = None
    goalkeeperPointX: float | None = None
    goalkeeperPointY: float | None = None
    id: str | None = None
    keeperTouchPointX: float | None = None
    keeperTouchPointY: float | None = None
    keeperTouchType: BodyType | None = None
    period: str | None = None
    possessionEvent: PFF_PossessionEvent | None = None
    pressurePlayer: Player | None = None
    pressureType: PressureType | None = None
    saveHeightType: ShotHeightType | None = None
    savePointX: float | None = None
    savePointY: float | None = None
    saveReboundType: SaveReboundType | None = None
    saverPlayer: Player | None = None
    shooterPlayer: Player | None = None
    shotBodyType: BodyType | None = None
    shotInitialHeightType: ShotHeightType | None = None
    shotNatureType: ShotNatureType | None = None
    shotOutcomeType: ShotOutcomeType | None = None
    shotPointX: float | None = None
    shotPointY: float | None = None
    shotTargetPointX: float | None = None
    shotTargetPointY: float | None = None


class PFF_Pitch(BaseModel):
    length: float | None = None
    width: float | None = None
    grassType: StadiumGrassType | None = None


class Stadium(BaseModel):
    id: str | None = None
    name: str | None = None
    pitches: list[PFF_Pitch] | None = Field(default_factory=list)


class Team(BaseModel):
    id: str | None = None
    name: str | None = None
    shortName: str | None = None


class PFF_Game(BaseModel):
    model_config = ConfigDict(validate_default=True, allow_none=True)

    id: str | int | None = None
    allRosters: list[Roster] | None = Field(default_factory=list)
    awayTeam: Team | None = None
    homeTeam: Team | None = None
    competition: Competition | None = None
    complete: bool | None = None
    date: str | None = None
    endPeriod1: float | None = None
    endPeriod2: float | None = None
    gameEvents: list[PFF_Event] | None = Field(default_factory=list)
    rosters: list[Roster] | None = Field(default_factory=list)
    season: str | int | None = None
    stadium: Stadium | None = None
    startPeriod1: float | None = None
    startPeriod2: float | None = None
    week: int | None = None

    def get_by_event_type(self, event_type: PFF_EventType) -> list[PFF_Event]:
        if not self.gameEvents:
            return []

        return [evt for evt in self.gameEvents if evt.gameEventType == event_type]

    def get_by_possession_event_type(
        self, possession_event_type: PFF_PossessionEventType
    ) -> list[PFF_Event]:
        if not self.gameEvents:
            return []

        return [
            evt
            for evt in self.gameEvents
            if evt.possessionEvents
            and any(
                (p_evt.possessionEventType == possession_event_type)
                for p_evt in evt.possessionEvents
            )
        ]


class PFF_Event(BaseModel):
    # model_config = ConfigDict(use_enum_values=False)
    id: str | int | None = None
    bodyType: BodyType | None = None
    defenderLocations: list[Location] | None = Field(default_factory=list)
    duration: float | None = None
    endPointX: float | None = None
    endPointY: float | None = None
    endTime: float | None = None
    endType: EndType | None = None
    formattedGameClock: str | None = None
    game: PFF_Game | None = None
    gameClock: float | None = None
    gameEventType: PFF_EventType | None = None
    heightType: HeightType | None = None
    initialTouchType: InitialTouchType | None = None
    offenderLocations: list[Location] | None = Field(default_factory=list)
    otherPlayer: Player | None = None
    outType: OutType | None = None
    period: str | int | None = None
    player: Player | None = None
    playerOff: Player | None = None
    playerOffType: PlayerOffType | None = None
    playerOn: Player | None = None
    possessionEvents: list[PFF_PossessionEvent] | None = Field(default_factory=list)
    pressurePlayer: Player | None = None
    pressureType: PressureType | None = None
    setpieceType: SetpieceType | None = None
    startTime: float | None = None
    startCoordinates: list[float] | None = Field(default_factory=list)
    subType: SubType | None = None
    team: Team | None = None
    touches: int | None = None
    touchesInBox: int | None = None

    def get_by_possession_event_type(
        self, possession_event_type: PFF_PossessionEventType
    ) -> list[PFF_PossessionEvent]:
        if not self.possessionEvents:
            return []

        return [
            evt
            for evt in self.possessionEvents
            if evt.possessionEventType == possession_event_type
        ]

    def get_by_possession_event_id(
        self, possession_event_id: str
    ) -> list[PFF_PossessionEvent]:
        if not self.possessionEvents:
            return []

        return [evt for evt in self.possessionEvents if evt.id == possession_event_id]

    def get_possession_events(self) -> list[PFF_PossessionEvent]:
        if not self.possessionEvents:
            return []

        return self.possessionEvents

    def __repr__(self) -> str:
        return f'PFF_Event({self.id}) {self.possessionEvents}'
