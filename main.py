from typing import Any, Dict, List

from fastapi import FastAPI, Query

from cache.cache import cache_response
from categories import Category
from players.player_averages import PlayerAverages
from players.player_category_leader import PlayerCategoryLeader
from players.player_service import (
    create_player_summary_from_search_result,
    get_leaders,
    get_paginated_players,
    get_player,
    get_player_averages,
)
from players.player_summary import PlayerSummary
from players.player_summary_response import PlayerSummaryResponse
from teams.team import Team
from teams.team_service import get_all_teams, get_team_players

app = FastAPI()


@app.get("/players/categories", response_model=List[PlayerCategoryLeader])
@cache_response(expire_time_seconds=86400)
async def get_category_leaders(
    number_of_players: int = Query(...), category: Category = Query(...)
) -> List[PlayerCategoryLeader]:
    return await get_leaders(number_of_players=number_of_players, category=category)


@app.get("/players/search", response_model=List[PlayerSummary])
@cache_response(expire_time_seconds=604800)
async def get_players_by_search(keyword: str = Query(...)):
    return await create_player_summary_from_search_result(keyword)


@app.get("/players/{player_id}/career-averages", response_model=List[PlayerAverages])
@cache_response(expire_time_seconds=604800)
async def get_player_career_averages(
    player_id: int, per_mode="PerGame"
) -> List[PlayerAverages]:
    return await get_player_averages(player_id=player_id, per_mode=per_mode)


@app.get("/players/{player_id}", response_model=PlayerSummary)
@cache_response(expire_time_seconds=604800)
async def get_player_by_id(player_id: int) -> PlayerSummary:
    return await get_player(player_id)


@app.get("/players", response_model=PlayerSummaryResponse)
@cache_response(expire_time_seconds=604800)
async def get_all_players(page: int = 1, players_per_page: int = 10) -> Dict[str, Any]:
    return await get_paginated_players(page, players_per_page)


@app.get("/teams/{team_id}/players", response_model=List[PlayerSummary])
@cache_response(expire_time_seconds=604800)
async def get_players_by_team(team_id: int) -> List[PlayerSummary]:
    return await get_team_players(team_id)


@app.get("/teams", response_model=List[Team])
@cache_response(expire_time_seconds=1200000)
async def get_teams() -> List[Team]:
    return await get_all_teams()
