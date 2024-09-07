import logging

import pandas as pd

from ...utils import convert_types, setup_logging
from ..data_fetching import fetching_team_stats
from ..team_settings import team_stats_columns_type_mapping

setup_logging()
logger = logging.getLogger(__name__)


async def get_team_stats_df(stats_url: str) -> pd.DataFrame:
    """function to handle teams stats to a pandas DataFrame"""
    team_stats = await fetching_team_stats(stats_url)

    df = pd.DataFrame(team_stats)

    invalid_rows_count = df[df["games_played"] == "-"].shape[0]
    if invalid_rows_count > 0:
        logger.debug(f"\nDropping {invalid_rows_count} rows with invalid 'games_played' values\n")
        df = df[df["games_played"] != "-"]

    combined_type_mapping: dict[str, type] = {"team_name": str, "games_played": int}

    for mapping in team_stats_columns_type_mapping:
        combined_type_mapping.update(mapping)

    df = convert_types(df, combined_type_mapping)
    return df
