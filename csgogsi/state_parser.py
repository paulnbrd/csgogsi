"""
To parse the json sent by CS:GO and store the payload as a dataclass object,
see Payload definition to see what you can retrieve from it
"""
from dataclasses import dataclass
import typing
import csgogsi.constants as constants


@dataclass
class MapTeam:
    score: int
    consecutive_round_losses: int
    timeouts_remaining: int
    matches_won_this_series: int


@dataclass
class Map:
    round_wins: typing.List[str]
    mode: str
    name: str
    phase: str
    round_no: int
    team_ct: MapTeam
    team_t: MapTeam
    num_matches_to_win_series: int
    current_spectators: int
    souvenirs_total: int


@dataclass
class Bomb:
    state: str
    position: tuple
    player: int


@dataclass
class PlayerMatchStats:
    kills: int
    assists: int
    deaths: int
    mvps: int
    score: int


@dataclass
class PlayerState:
    health: int
    armor: int
    helmet: bool
    flashed: int
    smoked: int
    burning: int
    money: int
    round_kills: int
    round_killhs: int
    round_totaldmg: int
    equip_value: int


@dataclass
class PlayerWeapon:
    name: str
    paintkit: str
    weapon_type: str
    state: str  # active, holstered
    ammo_clip: int
    ammo_clip_max: int
    ammo_reserve: int


@dataclass
class ObservedPlayer:
    steamid: int
    name: str
    clan: str
    observer_slot: int
    team: str
    activity: str
    match_stats: PlayerMatchStats
    state: PlayerState
    weapons: typing.List[PlayerWeapon]
    observed: int
    position: typing.Tuple[int]
    forward: typing.Tuple[int]


@dataclass
class Round:
    phase: str
    bomb: str
    win_team: str


@dataclass
class EndedRound:
    win_cause: str


@dataclass
class Provider:
    name: str
    appid: int
    version: int
    steamid: int
    timestamp: int


@dataclass
class Payload:
    raw_payload: dict
    provider: Provider
    played_map: Map
    current_round: Round
    player: ObservedPlayer
    allplayers: typing.List[ObservedPlayer]
    bomb: Bomb


CURRENT_PAYLOAD = constants.NULL


def get_payload_attr(*attrs, default=constants.NULL):
    global CURRENT_PAYLOAD
    if CURRENT_PAYLOAD != constants.NULL and CURRENT_PAYLOAD is not None:
        value = default
        sub = CURRENT_PAYLOAD.copy()
        for i in list(attrs):
            if i in sub.keys():
                # print("found {}".format(sub[i]))
                sub = sub[i]
            else:
                break
        else:
            value = sub
        return value
    else:
        return default


def parse_payload(payload: dict):
    global CURRENT_PAYLOAD
    CURRENT_PAYLOAD = payload

    # MAP
    _round_wins = get_payload_attr("map", "round_wins")
    if _round_wins != constants.NULL:
        round_wins = [i for i in _round_wins.values()]
    else:
        round_wins = []

    mode = get_payload_attr("map", "mode")
    name = get_payload_attr("map", "name")
    phase = get_payload_attr("map", "phase")
    round_no = get_payload_attr("map", "round")
    team_ct = MapTeam(
        score=get_payload_attr("map", "team_ct", "score"),
        consecutive_round_losses=get_payload_attr("map", "team_ct", "consecutive_round_losses"),
        timeouts_remaining=get_payload_attr("map", "team_ct", "timeouts_remaining"),
        matches_won_this_series=get_payload_attr("map", "team_ct", "matches_won_this_series")
    )
    team_t = MapTeam(
        score=get_payload_attr("map", "team_t", "score"),
        consecutive_round_losses=get_payload_attr("map", "team_t", "consecutive_round_losses"),
        timeouts_remaining=get_payload_attr("map", "team_t", "timeouts_remaining"),
        matches_won_this_series=get_payload_attr("map", "team_t", "matches_won_this_series")
    )

    num_matches_to_win_series = get_payload_attr("map", "num_matches_to_win_series")
    current_spectators = get_payload_attr("map", "current_spectators")
    souvenirs_total = get_payload_attr("map", "souvenirs_total")

    played_map = Map(round_wins=round_wins,
                     mode=mode,
                     name=name,
                     phase=phase,
                     round_no=round_no,
                     team_ct=team_ct,
                     team_t=team_t,
                     num_matches_to_win_series=num_matches_to_win_series,
                     current_spectators=current_spectators,
                     souvenirs_total=souvenirs_total)
    current_round = Round(
        phase=get_payload_attr("round", "phase"),
        bomb=get_payload_attr("round", "bomb", default=constants.BOMB_CARRIED),
        win_team=get_payload_attr("round", "win_team", default=constants.NULL)
    )
    # print(current_round.bomb)

    match_stats = PlayerMatchStats(
        kills=get_payload_attr("player", "match_stats", "kills"),
        assists=get_payload_attr("player", "match_stats", "assists"),
        deaths=get_payload_attr("player", "match_stats", "deaths"),
        mvps=get_payload_attr("player", "match_stats", "mvps"),
        score=get_payload_attr("player", "match_stats", "score")
    )
    player_state = PlayerState(
        health=get_payload_attr("player", "state", "health"),
        armor=get_payload_attr("player", "state", "armor"),
        helmet=get_payload_attr("player", "state", "helmet"),
        flashed=get_payload_attr("player", "state", "flashed"),
        smoked=get_payload_attr("player", "state", "smoked"),
        burning=get_payload_attr("player", "state", "burning"),
        money=get_payload_attr("player", "state", "money"),
        round_kills=get_payload_attr("player", "state", "round_kills"),
        round_killhs=get_payload_attr("player", "state", "round_killhs"),
        round_totaldmg=get_payload_attr("player", "state", "round_totaldmg"),
        equip_value=get_payload_attr("player", "state", "equip_value")
    )
    _weapons = get_payload_attr("player", "weapons")
    weapons = []
    if _weapons != constants.NULL:
        for i in _weapons.keys():
            weapons.append(PlayerWeapon(
                name=get_payload_attr("player", "weapons", i, "name"),
                paintkit=get_payload_attr("player", "weapons", i, "paintkit"),
                weapon_type=get_payload_attr("player", "weapons", i, "type"),
                state=get_payload_attr("player", "weapons", i, "state"),
                ammo_clip=get_payload_attr("player", "weapons", i, "ammo_clip", default=0),
                ammo_clip_max=get_payload_attr("player", "weapons", i, "ammo_clip_max", default=0),
                ammo_reserve=get_payload_attr("player", "weapons", i, "ammo_reserve", default=0)
            ))
    player_pos = get_payload_attr("player", "position")
    if player_pos != constants.NULL:
        try:
            player_pos = tuple(float(i) for i in player_pos.split(", "))
        except AttributeError:
            pass
    player_forward = get_payload_attr("player", "forward")
    if player_forward != constants.NULL:
        try:
            player_forward = tuple(float(i) for i in player_forward.split(", "))
        except AttributeError:
            pass
    player = ObservedPlayer(
        steamid=get_payload_attr("player", "steamid", default=constants.NULL),
        name=get_payload_attr("player", "name", default=constants.NAME_UNCONNECTED),
        clan=get_payload_attr("player", "clan"),
        observer_slot=get_payload_attr("player", "observer_slot", default=constants.NULL),
        team=get_payload_attr("player", "team", default=constants.NO_TEAM),
        activity=get_payload_attr("player", "activity", default=constants.PLAYER_ACTIVITY_UNKNOWN),
        match_stats=match_stats,
        state=player_state,
        weapons=weapons,
        observed=get_payload_attr("player", "spectarget"),
        position=player_pos,
        forward=player_forward
    )

    allplayers = constants.NOT_IMPLEMENTED_YET  # Honestly, is it useful ? Yes. I'm going to implement it soon (maybe)

    bomb_pos = get_payload_attr("bomb", "position")
    if bomb_pos != constants.NULL:
        try:
            bomb_pos = tuple(float(i) for i in bomb_pos.split(", "))
        except AttributeError:
            pass
    bomb = Bomb(
        state=get_payload_attr("bomb", "state", default=constants.BOMB_CARRIED),
        position=bomb_pos,
        player=get_payload_attr("bomb", "player")
    )

    provider = Provider(
        name=get_payload_attr("provider", "name"),
        appid=get_payload_attr("provider", "appid"),
        version=get_payload_attr("provider", "version"),
        steamid=get_payload_attr("provider", "steamid"),
        timestamp=get_payload_attr("provider", "timestamp")
    )

    payload = Payload(raw_payload=payload, provider=provider, played_map=played_map, current_round=current_round, player=player,
                      allplayers=allplayers, bomb=bomb)
    return payload
