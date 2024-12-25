from test.all_teams_data import MOCK_TEAMS
from typing import List
from unittest.mock import patch

import pytest
from fastapi import Response
from fastapi.testclient import TestClient

from main import app


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
