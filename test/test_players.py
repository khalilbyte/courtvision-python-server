from typing import Any, Dict, List
from unittest.mock import patch

import pytest
from fastapi import Response
from fastapi.testclient import TestClient

from categories import Category
from main import app
from players.player_summary import PlayerSummary

MOCK_PLAYER_IDS = [1630173, 203500]

MOCK_PLAYERS = [
    PlayerSummary(
        player_id=1630173,
        first_name="Precious",
        last_name="Achiuwa",
        birth_date="1999-09-19",
        height="6-8",
        weight="225",
        season_exp=2,
        jersey="5",
        position="F",
        team_id=1610612761,
        team_city="New York",
        team_name="Knicks",
    ),
    PlayerSummary(
        player_id=203500,
        first_name="Steven",
        last_name="Adams",
        birth_date="1993-07-20",
        height="6-11",
        weight="265",
        season_exp=9,
        jersey="4",
        position="C",
        team_id=1610612763,
        team_city="Memphis",
        team_name="Grizzlies",
    ),
]


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def mock_get_player_info():
    async def _mock_get_player_info(player_id: int) -> PlayerSummary:
        for player in MOCK_PLAYERS:
            if player.player_id == player_id:
                return player
        raise ValueError(f"No player found with ID: {player_id}")

    return _mock_get_player_info


@pytest.fixture
def mock_get_all_player_ids():
    async def _mock_get_all_player_ids() -> List[int]:
        return MOCK_PLAYER_IDS

    return _mock_get_all_player_ids


@pytest.fixture
def mock_get_leaders():
    async def _mock_get_leaders(
        number_of_players: int, category: Category
    ) -> List[List]:
        MOCK_PLAYERS: List[List] = [
            [
                203507,
                1,
                "Giannis Antetokounmpo",
                1610612749,
                "MIL",
                24,
                35.0,
                12.8,
                20.9,
                0.613,
                0.2,
                0.8,
                0.222,
                7.0,
                11.3,
                0.614,
                2.0,
                9.6,
                11.6,
                6.0,
                0.7,
                1.5,
                3.4,
                32.7,
                36.6,
            ],
            [
                1628983,
                2,
                "Shai Gilgeous-Alexander",
                1610612760,
                "OKC",
                30,
                34.7,
                10.8,
                21.0,
                0.517,
                2.2,
                6.2,
                0.348,
                7.0,
                8.0,
                0.879,
                0.9,
                4.7,
                5.6,
                6.1,
                2.0,
                1.1,
                2.7,
                30.8,
                31.8,
            ],
        ]
        return MOCK_PLAYERS

    return _mock_get_leaders


# /players/categories endpoint tests
@pytest.mark.asyncio
async def test_get_leaders(client: TestClient, mock_get_leaders) -> None:
    number_of_players: int = 2
    category: Category = Category.points

    with patch(
        "players.player_service.get_leaders",
        new=mock_get_leaders,
    ):
        response: Response = client.get(
            f"/players/categories",
            params={"number_of_players": number_of_players, "category": category.value},
        )

        assert response.status_code == 200
        mock_response = await mock_get_leaders(number_of_players, category)
        data = response.json()

        assert len(data) == len(mock_response)
        assert data[0][0] == mock_response[0][0]
        assert data[0][1] == mock_response[0][1]
        assert data[0][2] == mock_response[0][2]
        assert data[1][0] == mock_response[1][0]
        assert data[1][1] == mock_response[1][1]
        assert data[1][2] == mock_response[1][2]


# /players/search endpoint tests
@pytest.mark.asyncio
async def test_get_players_by_search(client: TestClient, mock_get_player_info) -> None:
    search_keyword = "Precious"

    mock_search_result = [
        {
            "id": 1630173,
            "first_name": "Precious",
            "last_name": "Achiuwa",
            "is_active": True,
        }
    ]

    with patch(
        "players.player_service.search_players", return_value=mock_search_result
    ), patch("players.player_service.get_player_info", new=mock_get_player_info):

        response: Response = client.get(
            f"/players/search", params={"keyword": search_keyword}
        )

        assert response.status_code == 200
        data = response.json()

        assert len(data) == 1
        assert data[0]["player_id"] == 1630173
        assert data[0]["first_name"] == "Precious"
        assert data[0]["last_name"] == "Achiuwa"


# /players/{player_id} endpoint tests
@pytest.mark.asyncio
async def test_get_player_by_id(client: TestClient, mock_get_player_info) -> None:
    with patch("players.player_service.get_player_info", new=mock_get_player_info):
        response: Response = client.get("/players/1630173")

        assert response.status_code == 200
        data = response.json()

        assert data["player_id"] == 1630173
        assert data["first_name"] == "Precious"
        assert data["last_name"] == "Achiuwa"
        assert data["team_city"] == "New York"
        assert data["team_name"] == "Knicks"


@pytest.mark.asyncio
async def test_get_player_by_id_not_found(
    client: TestClient, mock_get_player_info
) -> None:
    with patch("players.player_service.get_player_info", new=mock_get_player_info):
        response: Response = client.get("/players/99999")

        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"].lower()


# /players endpoint tests
@pytest.mark.asyncio
async def test_get_all_players(
    client: TestClient, mock_get_all_player_ids, mock_get_player_info
) -> None:
    with patch(
        "players.player_service.get_all_player_ids", new=mock_get_all_player_ids
    ), patch("players.player_service.get_player_info", new=mock_get_player_info):
        response: Response = client.get(
            "/players", params={"page": 1, "players_per_page": 2}
        )

        assert response.status_code == 200
        data: Dict[str, Any] = response.json()

        players: List[Dict[str, Any]] = data["players"]
        assert players[0]["player_id"] == 1630173
        assert players[0]["first_name"] == "Precious"
        assert players[0]["last_name"] == "Achiuwa"

        assert players[1]["player_id"] == 203500
        assert players[1]["first_name"] == "Steven"
        assert players[1]["last_name"] == "Adams"

        assert data["current_page"] == 1
        assert data["previous_page"] is None
        assert data["next_page"] is None
        assert data["is_last_page"]
        assert len(data["players"]) == 2


@pytest.mark.asyncio
async def test_all_players_invalid_parameters(
    client: TestClient, mock_get_all_player_ids, mock_get_player_info
) -> None:
    with patch(
        "players.player_service.get_all_player_ids", new=mock_get_all_player_ids
    ), patch("players.player_service.get_player_info", new=mock_get_player_info):
        response: Response = client.get(
            "/players", params={"page": 15, "players_per_page": 9999}
        )

        assert response.status_code == 200
        data: Dict[str, Any] = response.json()

        assert data["current_page"] == 1
        assert data["previous_page"] is None
        assert data["next_page"] is None
        assert data["is_last_page"]
        assert len(data["players"]) == 2


@pytest.mark.asyncio
async def test_min_players_per_page(
    client: TestClient, mock_get_all_player_ids, mock_get_player_info
) -> None:
    with patch(
        "players.player_service.get_all_player_ids", new=mock_get_all_player_ids
    ), patch("players.player_service.get_player_info", new=mock_get_player_info):
        response: Response = client.get(
            "/players", params={"page": 1, "players_per_page": 1}
        )

        assert response.status_code == 200
        data: Dict[str, Any] = response.json()

        assert len(data["players"]) == 1
        assert data["total_players"] == len(MOCK_PLAYER_IDS)
        assert not data["is_last_page"]


@pytest.mark.asyncio
async def test_exact_max_players_per_page(
    client: TestClient, mock_get_all_player_ids, mock_get_player_info
) -> None:
    with patch(
        "players.player_service.get_all_player_ids", new=mock_get_all_player_ids
    ), patch("players.player_service.get_player_info", new=mock_get_player_info):
        response: Response = client.get(
            "/players", params={"page": 1, "players_per_page": 50}
        )

        assert response.status_code == 200
        data: Dict[str, Any] = response.json()

        assert len(data["players"]) == len(MOCK_PLAYER_IDS)
        assert data["is_last_page"]


@pytest.mark.asyncio
async def test_last_page_indicators(
    client: TestClient, mock_get_all_player_ids, mock_get_player_info
) -> None:
    with patch(
        "players.player_service.get_all_player_ids", new=mock_get_all_player_ids
    ), patch("players.player_service.get_player_info", new=mock_get_player_info):
        response: Response = client.get(
            "/players", params={"page": 2, "players_per_page": 1}
        )

        assert response.status_code == 200
        data: Dict[str, Any] = response.json()

        assert data["current_page"] == 2
        assert data["previous_page"] == 1
        assert data["next_page"] is None
        assert data["is_last_page"]
