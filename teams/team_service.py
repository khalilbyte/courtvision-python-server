import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List

from fastapi import HTTPException, status
from nba_api.stats.static.teams import get_teams

from players.player_service import get_all_team_players
from players.player_summary import PlayerSummary
from teams.team import Team

executor: ThreadPoolExecutor = ThreadPoolExecutor()


# Core Team Functions
async def get_all_teams() -> List[Team]:
    try:
        teams_data: List[dict] = await get_all_team_data()
        teams: List[Team] = []

        for data in teams_data:
            team: Team = Team(
                team_id=data["id"],
                full_name=data["full_name"],
                abbreviation=data["abbreviation"],
                nickname=data["nickname"],
                city=data["city"],
            )
            teams.append(team)
        return teams
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )


async def get_all_team_data() -> List[Dict]:
    try:
        loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
        nba_teams: List[Dict] = await loop.run_in_executor(executor, get_teams)
        return nba_teams
    except asyncio.CancelledError:
        raise
    except Exception as e:
        raise RuntimeError(f"Failed to fetch team data: {str(e)}")


# Team Player Functions
async def get_team_players(team_id: int) -> List[PlayerSummary]:
    return await get_all_team_players(team_id)
