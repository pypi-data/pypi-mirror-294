import pandas as pd

from ...utils import convert_types
from ..data_fetching import fetching_player_stats
from ..player_settings import player_stats_columns_type_mapping


async def get_players_stats_df(stats_url: str) -> pd.DataFrame:
    """COnstruct pandas Dataframe of players data"""
    player_stats = await fetching_player_stats(stats_url)

    df = pd.DataFrame(player_stats)

    # Split the player_name into lastname_initials and first_name
    df[["lastname_initials", "first_name"]] = df["player_name"].str.split(pat=" ", n=1, expand=True)

    combined_type_mapping = {"player_name": str, "school": str, "games_played": int, "games_started": int}

    for mapping in player_stats_columns_type_mapping:
        combined_type_mapping.update(mapping)

    df = convert_types(df, combined_type_mapping)
    df = df.drop(columns=["player_name"])
    return df
