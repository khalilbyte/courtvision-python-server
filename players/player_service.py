import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List

from nba_api.stats.endpoints.leagueleaders import LeagueLeaders
from player_category_leader import PlayerCategoryLeader

from categories import Category

executor: ThreadPoolExecutor = ThreadPoolExecutor()


async def get_category_leaders(
    number_of_leaders: int, category: Category
) -> List[PlayerCategoryLeader]:
    if number_of_leaders <= 0:
        number_of_leaders = 5

    # Have to make sure we don't overwhelm the NBA API
    if number_of_leaders > 20:
        number_of_leaders = 20

    logging.debug(number_of_leaders)

    category_leaders: LeagueLeaders = LeagueLeaders(
        per_mode48="PerGame", stat_category_abbreviation=category.value
    )

    loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
    with executor as thread_pool:
        try:
            # NBA library isn't async so we will run blocking call in separate thread
            category_leaders: Dict = await loop.run_in_executor(
                executor=thread_pool, func=category_leaders.get_dict
            )

            result_set: List = category_leaders.get("resultSet")
            if not result_set or "rowSet" not in result_set:
                logging.error(
                    f"NBA API response structure is invalid: {category_leaders}"
                )
                raise RuntimeError("NBA API returned an invalid response structure")

            list_of_leaders: List[List] = result_set["rowSet"][:number_of_leaders]
            logging.debug(f"Fetched {len(list_of_leaders)} leader entries")

            processed_category_leaders: List = await asyncio.gather(
                *(create_category_leader(player) for player in list_of_leaders)
            )

            return processed_category_leaders

        except asyncio.CancelledError:
            raise
        except Exception as e:
            logging.exception("Error fetching category leaders")
            raise RuntimeError(f"Failed to fetch players: {str(e)}") from e


async def create_category_leader(player_data: List) -> PlayerCategoryLeader:
    try:
        return PlayerCategoryLeader(
            player_id=player_data[0],
            player_name=player_data[2],
            rank=player_data[1],
            team_id=player_data[3],
            games_played=player_data[5],
            minutes_played=player_data[6],
            fgm=player_data[7],
            fga=player_data[8],
            fgpct=player_data[9],
            fg3m=player_data[10],
            fg3a=player_data[11],
            fg3_pct=player_data[12],
            ftm=player_data[13],
            fta=player_data[14],
            ftpct=player_data[15],
            oreb=player_data[16],
            dreb=player_data[17],
            reb=player_data[18],
            ast=player_data[19],
            stl=player_data[20],
            blk=player_data[21],
            tov=player_data[22],
            pts=player_data[23],
            eff=player_data[24],
        )
    except (IndexError, KeyError) as e:
        logging.error(f"Invalid player data format: {player_data}")
        raise ValueError(f"Invalid player data format: {str(e)}") from e
    except ValueError as e:
        logging.error(
            f"Error processing player data: {str(e)}, Data: {player_data}",
            str(e),
            player_data,
        )
        raise
