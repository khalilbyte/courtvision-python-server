from enum import Enum


class Category(str, Enum):
    points = "PTS"
    rebounds = "REB"
    assists = "AST"
    blocks = "BLK"
    steals = "STL"
