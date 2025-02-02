from pydantic import BaseModel, computed_field

from teams.team_grouping import TEAMS_BY_ID


class PlayerSummary(BaseModel):
    player_id: int = 0
    first_name: str | None = None
    last_name: str | None = None
    birth_date: str | None = None
    height: str | None = None
    weight: str | None = None
    season_exp: int = 0
    jersey: str | None = None
    position: str | None = None
    team_id: int = 0
    team_city: str | None = None
    team_name: str | None = None

    @computed_field
    @property
    def conference(self) -> str:
        return TEAMS_BY_ID.get(self.team_name, TEAMS_BY_ID[None])["conference"]

    @computed_field
    @property
    def division(self) -> str:
        return TEAMS_BY_ID.get(self.team_name, TEAMS_BY_ID[None])["division"]

    @computed_field
    @property
    def player_image_url(self) -> str | None:
        return f"https://cdn.nba.com/headshots/nba/latest/1040x760/{self.player_id}.png"

    @computed_field
    @property
    def team_image_url(self) -> str | None:
        if self.team_id is None or self.team_id == 0:
            return "https://cdn.worldvectorlogo.com/logos/nba-6.svg"
        return f"https://cdn.nba.com/logos/nba/{self.team_id}/global/L/logo.svg"
