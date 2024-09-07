"""Test for team stats to work as expected"""

from pandas import DataFrame, Series

from usports_basketball import usport_teams_stats

from .test_data import expected_reg_season_column_names, men_team_victoria_2023_stats


def test_usports_team_stats():
    """Test if usport_teams_stats returns a valid DataFrame with expected columns and matching row data."""

    team_stats_df = usport_teams_stats("men")

    # Check DataFrame type and non-emptiness
    assert isinstance(team_stats_df, DataFrame), "Expected a pandas DataFrame."
    assert not team_stats_df.empty, "DataFrame is empty."

    actual_columns = team_stats_df.columns.tolist()
    for column in expected_reg_season_column_names:
        assert column in actual_columns, f"Column '{column}' missing."

    def row_matches(expected_row: dict, actual_row: Series) -> bool:
        """Check if the actual row contains expected values."""
        for key, value in expected_row.items():
            if key in actual_row and actual_row[key] == value:
                return True
        return False

    match_found = any(row_matches(men_team_victoria_2023_stats, row) for index, row in team_stats_df.iterrows())
    assert match_found, "No row matches the expected team statistics"
