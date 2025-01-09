from typing import Optional


class PlayersNotFoundException(Exception):
    def __init__(self, message: Optional[str] = None) -> None:
        self.message = message or f"Players not found"
        super().__init__(self.message)
