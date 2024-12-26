import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import Any, Callable, Dict, List

from dateutil import parser
from fastapi import HTTPException, status
from nba_api.stats.endpoints.commonplayerinfo import CommonPlayerInfo
from nba_api.stats.endpoints.commonteamroster import CommonTeamRoster
from nba_api.stats.static.players import get_active_players
from nba_api.stats.static.teams import _find_team_name_by_id, get_teams

from players.player_summary import PlayerSummary

executor: ThreadPoolExecutor = ThreadPoolExecutor()


async def get_all_player_ids() -> List[int]:
    loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
    active_nba_players: List[dict] = await loop.run_in_executor(
        executor, get_active_players
    )
    return [player["id"] for player in active_nba_players]


async def get_all_team_data() -> List[dict]:
    loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
    nba_teams: List[dict] = await loop.run_in_executor(executor, get_teams)
    return nba_teams


async def get_player_info(player_id: int) -> PlayerSummary:
    loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()

    try:
        get_info: Callable[[], CommonPlayerInfo] = partial(CommonPlayerInfo, player_id)
        common_player_info = await loop.run_in_executor(executor, get_info)
        response = await loop.run_in_executor(executor, common_player_info.get_dict)

        if not response.get("resultSets") or not response["resultSets"][0].get(
            "rowSet"
        ):
            return PlayerSummary()

        data = response["resultSets"][0]["rowSet"][0]

        return PlayerSummary(
            player_id=data[0],
            first_name=data[1],
            last_name=data[2],
            birth_date=data[7],
            height=data[11],
            weight=data[12],
            season_exp=data[13],
            jersey=data[14],
            position=data[15],
            team_id=data[18],
            team_city=data[22],
            team_name=data[19],
        )

    except Exception:
        return PlayerSummary()


async def get_all_team_players(team_id: int) -> List[PlayerSummary]:
    team_data: Any = _find_team_name_by_id(team_id=team_id)

    if team_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The ID {team_id} is not a valid team ID",
        )

    loop = asyncio.get_running_loop()

    team_roster: CommonTeamRoster = CommonTeamRoster(team_id=team_id)
    roster_response: Dict = await loop.run_in_executor(
        executor, lambda: team_roster.common_team_roster.get_dict()
    )

    roster_data = roster_response["data"]

    async def create_player_summary(player_data: list) -> PlayerSummary:
        full_name = player_data[3]
        name_parts = full_name.split(" ", 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        return PlayerSummary(
            player_id=player_data[14],
            first_name=first_name,
            last_name=last_name,
            birth_date=parser.parse(player_data[10]).strftime("%Y-%m-%dT%H:%M:%S"),
            height=player_data[8],
            weight=player_data[9],
            season_exp=0 if player_data[12] == "R" else int(player_data[12]),
            jersey=player_data[2],
            position=player_data[7],
            team_id=player_data[0],
            team_city=team_data["city"],
            team_name=team_data["nickname"],
        )

    player_summaries = await asyncio.gather(
        *(create_player_summary(player) for player in roster_data)
    )

    return player_summaries
