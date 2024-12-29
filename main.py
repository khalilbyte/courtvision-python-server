from typing import Any, Dict, List

from fastapi import FastAPI, Query

from categories import Category
from players.player_service import (
    create_player_summary_from_search_result,
    get_leaders,
    get_paginated_players,
    get_player,
)
from players.player_summary import PlayerSummary
from players.player_summary_response import PlayerSummaryResponse
from teams.team import Team
from teams.team_service import get_all_teams, get_team_players

app = FastAPI()


@app.get("/players/categories", response_model=List[List])
async def get_category_leaders(
    number_of_players: int, category: Category
) -> List[List]:
    return await get_leaders(number_of_players=number_of_players, category=category)


@app.get("/players/search", response_model=List[PlayerSummary])
async def get_players_by_search(keyword: str = Query(...)):
    return await create_player_summary_from_search_result(keyword)


@app.get("/players/{player_id}", response_model=PlayerSummary)
async def get_player_by_id(player_id: int) -> PlayerSummary:
    return await get_player(player_id)


@app.get("/players", response_model=PlayerSummaryResponse)
async def get_all_players(page: int = 1, players_per_page: int = 10) -> Dict[str, Any]:
    return await get_paginated_players(page, players_per_page)


@app.get("/teams/{team_id}/players", response_model=List[PlayerSummary])
async def get_players_by_team(team_id: int) -> List[PlayerSummary]:
    return await get_team_players(team_id)


@app.get("/teams", response_model=List[Team])
async def get_teams() -> List[Team]:
    return await get_all_teams()
