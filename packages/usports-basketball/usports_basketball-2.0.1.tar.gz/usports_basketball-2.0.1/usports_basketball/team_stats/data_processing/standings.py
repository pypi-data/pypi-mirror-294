import pandas as pd

from ...utils import convert_types
from ..data_fetching import fetching_standings_data
from ..team_settings import standings_type_mapping


async def get_standings_df(standings_url: str) -> pd.DataFrame:
    """function to handle stadnings data into a pandas DataFrame"""
    # Fetch standings data
    standings_data, team_record_data = await fetching_standings_data(standings_url)
    
    standings_df = pd.DataFrame(standings_data)
    standings_df = convert_types(standings_df, standings_type_mapping)
    standings_df = standings_df.drop(columns=["ties"])

    # Convert team record data into a DataFrame
    team_record_df = pd.DataFrame(team_record_data)
    team_record_df[['home', 'away', 'streak']] = team_record_df[['home', 'away', 'streak']].astype(str)

    # Merge the two DataFrames based on the "team_name" column
    combined_df = pd.merge(standings_df, team_record_df, on="team_name", how="left")

    return combined_df
