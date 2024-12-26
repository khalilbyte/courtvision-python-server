from typing import List, Optional

from pydantic import BaseModel

from players.player_summary import PlayerSummary


class PlayerSummaryResponse(BaseModel):
    players: List[PlayerSummary]
    current_page: int
    next_page: Optional[int]
    previous_page: Optional[int]
    is_last_page: bool
    total_players: int
