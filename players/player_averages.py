from pydantic import BaseModel

# nba_api/stats/endpoints/playerprofilev2.py


class PlayerAverages(BaseModel):
    player_id: int = 0
    season_id: str | None = None
    team_id: int = 0
    team_abbreviation: str | None = None
    player_age: int = 0
    gp: int = 0
    gs: int = 0
    min: float = 0.0
    fgm: float = 0.0
    fga: float = 0.0
    fg_pct: float = 0.0
    fg3m: float = 0.0
    fg3a: float = 0.0
    fg3_pct: float = 0.0
    ftm: float = 0.0
    fta: float = 0.0
    ft_pct: float = 0.0
    oreb: float = 0.0
    dreb: float = 0.0
    reb: float = 0.0
    ast: float = 0.0
    stl: float = 0.0
    blk: float = 0.0
    tov: float = 0.0
    pf: float = 0.0
    pts: float = 0.0
