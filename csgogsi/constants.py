"""
Use these variable to easily compare the values of the payload
"""

NULL: int = -1
NOT_IMPLEMENTED_YET: Exception = NotImplemented

ROUND_WIN_T_BOMB: str = "t_win_bomb"
ROUND_WIN_T_ELIMINATIONS: str = "t_win_elimination"
ROUND_WIN_CT_DEFUSE: str = "ct_win_defuse"
ROUND_WIN_CT_ELIMINATIONS: str = "ct_win_elimination"

ROUND_PHASE_FREEZETIME: str = "freezetime"
ROUND_PHASE_LIVE: str = "live"
ROUND_PHASE_OVER: str = "over"

BOMB_CARRIED: str = "carried"
BOMB_PLANTING: str = "planting"
BOMB_PLANTED: str = "planted"
BOMB_DEFUSED: str = "defused"
BOMB_EXPLODED: str = "exploded"

WIN_TEAM_T: str = "T"
WIN_TEAM_CT: str = "CT"
TEAM_T: str = WIN_TEAM_T
TEAM_CT: str = WIN_TEAM_CT
NO_TEAM: str = ""

PLAYER_NO_CLAN: str = " No clan"  # Space useful: no clan can have a space in their name (I guess)

NAME_UNCONNECTED: int = -2

PLAYER_ACTIVITY_PLAYING: str = "playing"
PLAYER_ACTIVITY_MENU: str = "menu"
PLAYER_ACTIVITY_TEXTINPUT: str = "textinput"
PLAYER_ACTIVITY_UNKNOWN: str = "unknown"

WEAPON_HOLSTERED: str = "holstered"
WEAPON_INACTIVE: str = WEAPON_HOLSTERED
WEAPON_ACTIVE: str = "active"
