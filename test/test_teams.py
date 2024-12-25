from test.all_teams_data import MOCK_TEAMS
from typing import List
from unittest.mock import patch

import pytest
from fastapi import Response
from fastapi.testclient import TestClient

from main import app
from players.player_summary import PlayerSummary


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def mock_get_all_team_data():
    async def _mock_get_all_team_data() -> List[dict]:
        return MOCK_TEAMS

    return _mock_get_all_team_data


@pytest.mark.asyncio
async def test_get_all_teams(client: TestClient, mock_get_all_team_data) -> None:
    with patch("main.get_all_team_data", new=mock_get_all_team_data):
        response: Response = client.get("/teams")

        assert response.status_code == 200
        teams: List[dict] = response.json()

        assert len(teams) == 30
        assert teams[0]["team_id"] is not None
        assert teams[1]["team_id"] is not None
        assert teams[2]["team_id"] is not None
        assert teams[3]["team_id"] is not None
        assert teams[4]["team_id"] is not None


@pytest.mark.asyncio
async def test_get_players_by_team(client: TestClient) -> None:
    MOCK_PLAYER_DATA = [
        {
            "player_id": 2544,
            "first_name": "LeBron",
            "last_name": "James",
            "birth_date": "DEC 30, 1984",
            "height": "6-9",
            "weight": "250",
            "season_exp": 21,
            "jersey": "23",
            "position": "F",
            "team_id": 1610612747,
            "team_city": "Los Angeles",
            "team_name": "Lakers",
        }
    ]

    async def mock_get_all_team_players(team_id: int) -> List[PlayerSummary]:
        return [PlayerSummary(**player) for player in MOCK_PLAYER_DATA]

    with patch("main.get_all_team_players", new=mock_get_all_team_players):
        response: Response = client.get(f"/teams/1610612747/players")

        assert response.status_code == 200
        players = response.json()

        assert len(players) == 1
        player = players[0]
        assert player["player_id"] == 2544
        assert player["first_name"] == "LeBron"
        assert player["last_name"] == "James"
        assert player["team_id"] == 1610612747
        assert player["team_city"] == "Los Angeles"
        assert player["team_name"] == "Lakers"
