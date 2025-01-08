import asyncio
import json
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List

from fastapi import HTTPException, status
from nba_api.stats.endpoints import (
    LeagueDashPlayerStats,
    LeagueLeaders,
    PlayerProfileV2,
)
from nba_api.stats.static.players import find_player_by_id

from categories import Category

executor: ThreadPoolExecutor = ThreadPoolExecutor()

# player_profile: PlayerProfileV2 = PlayerProfileV2(1628983, per_mode36="PerGame")


# # We will use this line of code to get the actual data to fill the PLayerStats class
# player_profile_dict: Dict = player_profile.get_dict()
# player_results: Dict = player_profile_dict["resultSets"][0]["rowSet"][
#     -1
# ]  # Grabs the most recent season (listed as newest last)
# print(player_results)

# Testing get player by ID
player: Any = find_player_by_id(
    162898333
)  # Valid ID -> Returns player dict Invalid ID -> Returns None
print(player)


async def get_player_stats(player_id: int, per_mode="PerGame"):
    pass
    # Check to make sure player ID is valid (create a helper function to validate player IDs)
    # If it isn't valid throw PlayerNotFound exception
    # If it is valid, insert it into PlayerProfileV2()
    # Be sure to use try-catch, there could be timeout error or a network error, raise exception in those cases
    # player_results: Dict = player_profile_dict["resultSets"][0]["rowSet"][-1] will return stats of most recent season
    # player_results: Dict = player_profile_dict["resultSets"][0]["rowSet"] will return career averages


# async def get_category_leaders(
#     number_of_players: int, category: Category
# ) -> List[List]:
#     if number_of_players <= 0:
#         number_of_players = 5

#     if number_of_players > 10:
#         number_of_players = 10

#     category_leaders = LeagueLeaders(
#         per_mode48="PerGame", stat_category_abbreviation=category.value
#     )

#     loop = asyncio.get_running_loop()
#     with executor as thread_pool:
#         try:
#             category_leaders_dict: Dict = await loop.run_in_executor(
#                 executor=thread_pool, func=category_leaders.get_dict
#             )
#             return category_leaders_dict["resultSet"]["rowSet"][:number_of_players]
#         except Exception as e:
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail=f"Failed to fetch players: {str(e)}",
#             )


# print(asyncio.run(get_category_leaders(5, Category.points)))
# print(
#     LeagueLeaders(per_mode48="PerGame", stat_category_abbreviation="PTS").get_dict()[
#         "resultSet"
#     ]
# )
