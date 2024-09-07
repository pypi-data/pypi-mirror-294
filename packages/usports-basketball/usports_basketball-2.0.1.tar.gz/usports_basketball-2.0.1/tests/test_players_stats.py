"""Test for players function to worek as expected"""

from pandas import DataFrame, Series

from usports_basketball import usport_players_stats

from .test_data import expected_players_df_columns, wbb_player_stats_2023


def test_usports_player_stats():
    """Test if usport_players_stats function returns a non-empty pandas DataFrame."""

    player_stats_df = usport_players_stats("women")

    assert isinstance(player_stats_df, DataFrame), "Player statistics should be a pandas DataFrame"
    assert not player_stats_df.empty, "Player statistics DataFrame is empty"

    actual_columns = player_stats_df.columns.tolist()
    for column in expected_players_df_columns:
        assert column in actual_columns, f"Expected column '{column}' not found in player_stats_df"

    # Check if any row matches the expected player statistics
    def row_matches(expected_row: dict, actual_row: Series) -> bool:
        """Check if the actual row contains expected values."""
        for key, value in expected_row.items():
            if key in actual_row and actual_row[key] == value:
                return True
        return False

    match_found = any(row_matches(wbb_player_stats_2023, row) for index, row in player_stats_df.iterrows())
    assert match_found, "No row matches the expected player statistics"
