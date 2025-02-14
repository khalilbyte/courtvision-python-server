from typing import TypedDict, Union


class TeamInfo(TypedDict):
    conference: str
    division: str


TEAMS_BY_ID: dict[Union[int, None], TeamInfo] = {
    1610612737: {"conference": "Eastern", "division": "Southeast"},  # Hawks
    1610612738: {"conference": "Eastern", "division": "Atlantic"},  # Celtics
    1610612751: {"conference": "Eastern", "division": "Atlantic"},  # Nets
    1610612766: {"conference": "Eastern", "division": "Southeast"},  # Hornets
    1610612741: {"conference": "Eastern", "division": "Central"},  # Bulls
    1610612739: {"conference": "Eastern", "division": "Central"},  # Cavaliers
    1610612742: {"conference": "Western", "division": "Southwest"},  # Mavericks
    1610612743: {"conference": "Western", "division": "Northwest"},  # Nuggets
    1610612765: {"conference": "Eastern", "division": "Central"},  # Pistons
    1610612744: {"conference": "Western", "division": "Pacific"},  # Warriors
    1610612745: {"conference": "Western", "division": "Southwest"},  # Rockets
    1610612754: {"conference": "Eastern", "division": "Central"},  # Pacers
    1610612746: {"conference": "Western", "division": "Pacific"},  # Clippers
    1610612747: {"conference": "Western", "division": "Pacific"},  # Lakers
    1610612763: {"conference": "Western", "division": "Southwest"},  # Grizzlies
    1610612748: {"conference": "Eastern", "division": "Southeast"},  # Heat
    1610612749: {"conference": "Eastern", "division": "Central"},  # Bucks
    1610612750: {"conference": "Western", "division": "Northwest"},  # Timberwolves
    1610612740: {"conference": "Western", "division": "Southwest"},  # Pelicans
    1610612752: {"conference": "Eastern", "division": "Atlantic"},  # Knicks
    1610612760: {"conference": "Western", "division": "Northwest"},  # Thunder
    1610612753: {"conference": "Eastern", "division": "Southeast"},  # Magic
    1610612755: {"conference": "Eastern", "division": "Atlantic"},  # 76ers
    1610612756: {"conference": "Western", "division": "Pacific"},  # Suns
    1610612757: {"conference": "Western", "division": "Northwest"},  # Trail Blazers
    1610612758: {"conference": "Western", "division": "Pacific"},  # Kings
    1610612759: {"conference": "Western", "division": "Southwest"},  # Spurs
    1610612761: {"conference": "Eastern", "division": "Atlantic"},  # Raptors
    1610612762: {"conference": "Western", "division": "Northwest"},  # Jazz
    1610612764: {"conference": "Eastern", "division": "Southeast"},  # Wizards
    None: {"conference": "N/A", "division": "N/A"},
    0: {"conference": "N/A", "division": "N/A"},
}
