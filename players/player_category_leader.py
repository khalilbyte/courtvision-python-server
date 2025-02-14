from typing import Optional

from pydantic import BaseModel, computed_field

from teams.team_mappings import TEAMS_BY_ID


class PlayerCategoryLeader(BaseModel):
    player_id: int = 0
    player_name: Optional[str] = None
    rank: int = 0
    team_id: Optional[int] = None
    games_played: int = 0
    minutes_played: float = 0
    fgm: float = 0
    fga: float = 0
    fg_pct: float = 0
    fg3m: float = 0
    fg3a: float = 0
    fg3_pct: float = 0
    ftm: float = 0
    fta: float = 0
    ft_pct: float = 0
    oreb: float = 0
    dreb: float = 0
    reb: float = 0
    ast: float = 0
    stl: float = 0
    blk: float = 0
    tov: float = 0
    pts: float = 0
    eff: float = 0

    @computed_field
    @property
    def conference(self) -> str:
        return TEAMS_BY_ID.get(self.team_id, TEAMS_BY_ID[None])["conference"]

    @computed_field
    @property
    def division(self) -> str:
        return TEAMS_BY_ID.get(self.team_id, TEAMS_BY_ID[None])["division"]

    @computed_field
    @property
    def player_image_url(self) -> str:
        return f"https://cdn.nba.com/headshots/nba/latest/1040x760/{self.player_id}.png"

    @computed_field
    @property
    def team_image_url(self) -> str | None:
        if self.team_id is None or self.team_id == 0:
            return "https://cdn.worldvectorlogo.com/logos/nba-6.svg"
        return f"https://cdn.nba.com/logos/nba/{self.team_id}/global/L/logo.svg"
