from pydantic import BaseModel, computed_field

from teams.team_grouping import TEAMS_BY_ID


class Team(BaseModel):
    team_id: int | None = None
    full_name: str | None = None
    abbreviation: str | None = None
    nickname: str | None = None
    city: str | None = None

    @computed_field
    @property
    def team_image_url(self) -> str | None:
        if self.team_id is None or self.team_id == 0:
            return "https://cdn.worldvectorlogo.com/logos/nba-6.svg"
        return f"https://cdn.nba.com/logos/nba/{self.team_id}/global/L/logo.svg"

    @computed_field
    @property
    def conference(self) -> str:
        return TEAMS_BY_ID.get(self.team_id, TEAMS_BY_ID[self.team_id])["conference"]

    @computed_field
    @property
    def division(self) -> str:
        return TEAMS_BY_ID.get(self.team_id, TEAMS_BY_ID[self.team_id])["division"]
