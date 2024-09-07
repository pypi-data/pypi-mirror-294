"""Contains mappings and configurations for player statistics and their data payload."""

player_stats_columns_type_mapping: list[dict[str, type]] = [
    {
        "minutes_played": int,
        "field_goal_made": int,
        "field_goal_percentage": float,
        "three_pointers_made": int,
        "three_pointers_percentage": float,
        "free_throws_made": int,
        "free_throws_percentage": float,
        "total_points": int,
    },
    {
        "offensive_rebounds": int,
        "defensive_rebounds": int,
        "total_rebounds": int,
        "assists": int,
        "turnovers": int,
        "steals": int,
        "blocks": int,
    },
    {
        "personal_fouls": int,
        "disqualifications": int,
        "assist_to_turnover_ratio": float,
    },
]

sort_categories = [
    "pts",
    "gp",
    "gs",
    "min",
    "fgp",
    "fgpt",
    "fgp3",
    "fgpt3",
    "ftp",
    "ftpt",
    "oreb",
    "dreb",
    "treb",
    "ast",
    "to",
    "stl",
    "blk",
    "pf",
    "dq",
    "ato",
]
