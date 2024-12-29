from enum import Enum

Category = Enum(
    "Category",
    [
        ("points", "PTS"),
        ("rebounds", "REB"),
        ("assists", "AST"),
        ("blocks", "BLK"),
        ("steals", "STL"),
    ],
)
