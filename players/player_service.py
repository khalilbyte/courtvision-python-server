import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from math import ceil
from typing import Any, Callable, Dict, List, Optional

from dateutil import parser
from fastapi import HTTPException, status
from nba_api.stats.endpoints.commonplayerinfo import CommonPlayerInfo
from nba_api.stats.endpoints.commonteamroster import CommonTeamRoster
from nba_api.stats.endpoints.leagueleaders import LeagueLeaders
from nba_api.stats.endpoints.playerprofilev2 import PlayerProfileV2
from nba_api.stats.static.players import (
    find_player_by_id,
    find_players_by_full_name,
    get_active_players,
)
from nba_api.stats.static.teams import _find_team_name_by_id

from categories import Category
from players.player_averages import PlayerAverages
from players.player_category_leader import PlayerCategoryLeader
from players.player_not_found_exception import PlayerNotFoundException
from players.player_summary import PlayerSummary
from players.player_summary_response import PlayerSummaryResponse

executor: ThreadPoolExecutor = ThreadPoolExecutor()


# Core Player Functions
async def get_player(player_id: int) -> PlayerSummary:
    try:
        return await asyncio.wait_for(get_player_info(player_id), timeout=10.0)
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Failed to retrieve player details within timeout period",
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with ID {player_id} not found",
        )


async def get_player_info(player_id: int) -> PlayerSummary:
    try:
        loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
        get_info: Callable[[], CommonPlayerInfo] = partial(CommonPlayerInfo, player_id)

        common_player_info = await loop.run_in_executor(executor, get_info)
        response = await loop.run_in_executor(executor, common_player_info.get_dict)

        if not response.get("resultSets") or not response["resultSets"][0].get(
            "rowSet"
        ):
            raise PlayerNotFoundException(f"Player {player_id} not found")

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

    except asyncio.CancelledError:
        raise
    except KeyError as e:
        raise PlayerNotFoundException(
            f"Invalid data format for player {player_id}: {e}"
        )
    except Exception as e:
        raise RuntimeError(f"Failed to fetch player {player_id}: {str(e)}")


"""
This function is responsible for getting a player's career averages by season. It takes
in a player ID that must first be confirmed it belongs to a player. If the inputted player ID
doesn't belong to a player, it will return an empty list. If it does belong to a player, it 
returns a list of PlayerAverages objects.
"""


async def get_career_averages(player_id: int) -> List[PlayerAverages]:
    # PlayerAverages maps to the data provided by the PlayerProfileV2 class

    # This argument allows us to retrieve the stats in a per game format
    per_mode: str = "PerGame"

    # If the player ID is invalid return an empty list
    isValid: bool = is_player_id_valid(player_id=player_id)
    if not isValid:
        return []

    # If the player ID is valid
    # Create something to hold all the player's career season averages
    career_season_averages: List[LeagueLeaders] = []

    # The constructor PlayerProfileV2() makes a synchronous API call, we need to make sure we make it asynchronous
    # Create an asynchronous event loop
    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()

    try:
        # Grab the instance of the player profile asynchronously (switched from run_in_exectuor() because harder to test manual event loop management)
        player_profile: PlayerProfileV2 = await asyncio.to_thread(
            PlayerProfileV2, player_id=player_id, per_mode36=per_mode
        )
        # Store the player's career averages of every season
        season_averages: List[List] = player_profile.season_totals_regular_season.data[
            "data"
        ]
        # For every season, store those season numbers
        for season in season_averages:
            # Store season averages inside an instance of a PlayerAverages class
            (
                player_id,
                season_id,
                _,
                team_id,
                team_abbreviation,
                player_age,
                gp,
                gs,
                minutes,
                fgm,
                fga,
                fg_pct,
                fg3m,
                fg3a,
                fg3_pct,
                ftm,
                fta,
                ft_pct,
                oreb,
                dreb,
                reb,
                ast,
                stl,
                blk,
                tov,
                pf,
                pts,
            ) = season
            averages_for_season: PlayerAverages = PlayerAverages(
                player_id=player_id,
                season_id=season_id,
                team_id=team_id,
                team_abbreviation=team_abbreviation,
                player_age=player_age,
                gp=gp,
                gs=gs,
                minutes=minutes,
                fgm=fgm,
                fga=fga,
                fg_pct=fg_pct,
                fg3m=fg3m,
                fg3a=fg3a,
                fg3_pct=fg3_pct,
                ftm=ftm,
                fta=fta,
                ft_pct=ft_pct,
                oreb=oreb,
                dreb=dreb,
                reb=reb,
                ast=ast,
                stl=stl,
                blk=blk,
                tov=tov,
                pf=pf,
                pts=pts,
            )
            # Store the instance
            career_season_averages.append(averages_for_season)
        # Return the object holding all of the player's career averages by season
        return career_season_averages
    except ConnectionError as ce:
        # Handle connection problems
        print("A connection error occured: ", ce)
        return []
    except TimeoutError as t:
        # Handle timeout
        print("A timeout error occured: ", t)
        return []
    except Exception as e:
        # Handle other request-related errors
        print("An error occured: ", e)
        return []


# Player List/Search Functions
async def get_paginated_players(
    page: int = 1, players_per_page: int = 10
) -> PlayerSummaryResponse:
    MAX_PLAYERS_PER_PAGE = 50
    MIN_PLAYERS_PER_PAGE = 1
    MIN_PAGE = 1

    if (
        players_per_page < MIN_PLAYERS_PER_PAGE
        or players_per_page > MAX_PLAYERS_PER_PAGE
    ):
        players_per_page = 10

    try:
        player_ids: List[int] = await asyncio.wait_for(
            get_all_player_ids(), timeout=10.0
        )
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Failed to retrieve player IDs within timeout period",
        )

    MAX_PAGE: int = ceil(len(player_ids) / players_per_page)

    if page < MIN_PAGE or page > MAX_PAGE:
        page = 1

    total_players: int = len(player_ids)
    total_pages: int = ceil(total_players / players_per_page)

    if page > total_pages:
        page = 1

    start: int = (page - 1) * players_per_page
    end: int = min(start + players_per_page, total_players)

    is_last_page: bool = page == total_pages
    next_page: Optional[int] = None if is_last_page else page + 1
    previous_page: Optional[int] = None if page == 1 else page - 1

    try:
        player_tasks = [get_player_info(id) for id in player_ids[start:end]]
        players: List[PlayerSummary] = await asyncio.wait_for(
            asyncio.gather(*player_tasks), timeout=15.0
        )
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Failed to retrieve player details within timeout period",
        )

    return PlayerSummaryResponse(
        players=players,
        current_page=page,
        next_page=next_page,
        previous_page=previous_page,
        is_last_page=is_last_page,
        total_players=total_players,
    )


async def get_leaders(
    number_of_players: int, category: Category
) -> List[PlayerCategoryLeader]:
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

            list_of_leaders: List[List] = category_leaders_dict["resultSet"]["rowSet"][
                :number_of_players
            ]
            processed_list = await asyncio.gather(
                *(create_player_category_leader(player) for player in list_of_leaders)
            )

            return processed_list
        except asyncio.CancelledError:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to fetch players: {str(e)}",
            )


async def create_player_category_leader(player_data: List):
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
        raise ValueError(f"Invalid player data format: {str(e)}")
    except ValueError as e:
        raise ValueError(f"Error processing player data: {str(e)}")


async def create_player_summary_from_search_result(
    keyword: str,
) -> List[PlayerSummary]:
    keywordCopy: str = str.strip(keyword)
    if keywordCopy == "" or keywordCopy.isalpha() == False or len(keywordCopy) < 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Value must be minimum 3 letters",
        )

    player_list: List[Dict] = search_players(keyword=keyword)
    filtered_player_list: List[Dict] = filter_active_players(players_list=player_list)

    players: List[PlayerSummary] = []

    try:
        for player in filtered_player_list:
            try:
                player_info: PlayerSummary = await get_player_info(
                    player_id=player["id"]
                )
                players.append(player_info)
            except PlayerNotFoundException:
                continue
        return players
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )


# Team Player Functions
async def get_all_team_players(team_id: int) -> List[PlayerSummary]:
    try:
        team_data: Any = _find_team_name_by_id(team_id=team_id)
        if team_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The ID {team_id} is not a valid team ID",
            )

        loop = asyncio.get_running_loop()
        team_roster: CommonTeamRoster = CommonTeamRoster(team_id=team_id)

        try:
            roster_response: Dict = await loop.run_in_executor(
                executor, lambda: team_roster.common_team_roster.get_dict()
            )
            roster_data = roster_response["data"]
        except KeyError:
            raise ValueError(f"Invalid roster data format for team {team_id}")

        player_summaries = await asyncio.gather(
            *(create_player_summary(player, team_data) for player in roster_data)
        )
        return player_summaries

    except asyncio.CancelledError:
        raise
    except Exception as e:
        raise RuntimeError(f"Failed to fetch team players for {team_id}: {str(e)}")


async def create_player_summary(player_data: List, team_data: Dict) -> PlayerSummary:
    try:
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
    except (IndexError, KeyError) as e:
        raise ValueError(f"Invalid player data format: {str(e)}")
    except ValueError as e:
        raise ValueError(f"Error processing player data: {str(e)}")


# Utility Functions
def is_player_id_valid(player_id: int) -> bool:
    if not isinstance(player_id, int):
        raise TypeError("The player_id argument must be an integer")

    try:
        player = find_player_by_id(player_id=player_id)
        if player is None:
            return False
        else:
            return True
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        return False


async def get_all_player_ids() -> List[int]:
    try:
        loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
        active_nba_players: List[Dict] = await loop.run_in_executor(
            executor, get_active_players
        )
        return [player["id"] for player in active_nba_players]
    except asyncio.CancelledError:
        raise
    except Exception as e:
        raise RuntimeError(f"Failed to fetch player IDs: {str(e)}")


def search_players(keyword: str) -> List[Dict]:
    return find_players_by_full_name(keyword)


def filter_active_players(players_list: List[Dict]) -> List:
    if players_list is None or len(players_list) == 0:
        return []

    active_players: List[Dict] = []
    for player in players_list:
        if player["is_active"]:
            active_players.append(player)

    return active_players
