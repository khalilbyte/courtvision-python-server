from nba_api.stats.endpoints.commonteamroster import CommonTeamRoster
from nba_api.stats.static.teams import _find_team_name_by_id

team_roster: CommonTeamRoster = CommonTeamRoster(1610612739)
print(team_roster.common_team_roster.get_dict()["data"])

team = _find_team_name_by_id(1610612739)
print(team)
