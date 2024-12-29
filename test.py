import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List

from fastapi import HTTPException, status
from nba_api.stats.endpoints import LeagueLeaders

from categories import Category

executor: ThreadPoolExecutor = ThreadPoolExecutor()


async def get_category_leaders(
    number_of_players: int, category: Category
) -> List[List]:
    if number_of_players <= 0:
        number_of_players = 5

    if number_of_players > 10:
        number_of_players = 10

    category_leaders = LeagueLeaders(
        per_mode48="PerGame", stat_category_abbreviation=category.value
    )

    loop = asyncio.get_running_loop()
    with executor as thread_pool:
        try:
            category_leaders_dict: Dict = await loop.run_in_executor(
                executor=thread_pool, func=category_leaders.get_dict
            )
            return category_leaders_dict["resultSet"]["rowSet"][:number_of_players]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch players: {str(e)}",
            )


print(asyncio.run(get_category_leaders(5, Category.points)))
# print(
#     LeagueLeaders(per_mode48="PerGame", stat_category_abbreviation="PTS").get_dict()[
#         "resultSet"
#     ]
# )
