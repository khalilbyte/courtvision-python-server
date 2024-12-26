import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import List

from dateutil import parser
from nba_api.stats.static.players import get_active_players

from util import get_all_player_ids

executor: ThreadPoolExecutor = ThreadPoolExecutor()


async def get_all_player_ids() -> List[int]:
    loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
    active_nba_players: List[dict] = await loop.run_in_executor(
        executor, get_active_players
    )
    print(len(active_nba_players))
    return [player["id"] for player in active_nba_players]


player_date: str = "JUN 19, 2003"
player_date_datetime: datetime = parser.parse(player_date)
print(player_date_datetime)
