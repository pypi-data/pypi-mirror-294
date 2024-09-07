# 🏀 usports-basketball 

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![PyPI Latest Release](https://img.shields.io/pypi/v/usports-basketball?color=orange)](https://pypi.org/project/usports-basketball/) 
[![License](https://img.shields.io/pypi/l/usports-basketball.svg)](https://github.com/ojadeyemi/usports-basketball/blob/main/LICENSE) 
[![Downloads](https://static.pepy.tech/badge/usports-basketball)](https://pepy.tech/project/usports-basketball) 
[![Package Status](https://img.shields.io/pypi/status/usports-basketball.svg)](https://pypi.org/project/usports-basketball/)

**usports-basketball** is a Python package that fetches and analyzes current basketball stats from the [U Sports website](https://usports.ca/en). 

With two simple functions you can easily retrieve detailed data for either the men's or women's league. 
- `usport_teams_stats`: Fetch team stats.
- `usport_players_stats`: Fetch player stats.

Each function returns a pandas DataFrame with the relevant statistics, allowing users to gather data for analysis and insights.

## 📥 Installation

You can install the package via pip:

```bash
pip install usports-basketball
```

## 🧩 Dependencies

This package relies on the following dependencies:

- pandas
- BeautifulSoup (bs4)
- requests
- pytest
- playwright

## Installing Chromium for Playwright

After installing the package, you'll need to install Playwright's Chromium browser. Run the following command:

```bash
playwright install chromium
```

## Functions

### `usport_teams_stats`

This function fetches and processes team statistics data, including standings, win-loss totals, shooting percentages, and other relevant team metrics for the current U Sports basketball season.

#### Parameters

- `arg` (str): The league for which you want to retrieve team statistics. Valid values are `'men'` and `'women'` or `'m'` and `'w'` (case-insensitive).
- `season_option` (str, optional): The season type to fetch data for. Options are:
  - `'regular'` (default): Regular season statistics.
  - `'playoffs'`: Playoff season statistics.
  - `'championship'`: Championship season statistics.

#### Returns

- `DataFrame`: A pandas DataFrame containing the team statistics data.

### `usports_player_stats`

This function fetches and processes player statistics data, including total games played, points scored, shooting percentages, rebounds, assists, turnovers, steals, blocks, and other individual player metrics for the current U Sports basketball season.

#### Parameters

- `arg` (str): The league for which you want to retrieve team statistics. Valid values are `'men'` and `'women'` or `'m'` and `'w'` (case-insensitive).
- `season_option` (str, optional): The season type to fetch data for. Options are:
  - `'regular'` (default): Regular season statistics.
  - `'playoffs'`: Playoff season statistics.
  - `'championship'`: Championship season statistics.

#### Returns

- `DataFrame`: A pandas DataFrame containing the player statistics data.

## Usage

- ### Fetching current stats from the league

```python
from usports_basketball import usport_teams_stats, usports_player_stats

# Fetching and processing men's team statistics
men_team_stats_df = usport_teams_stats('m')

# Fetching and processing men's player statistics
men_player_stats_df = usport_players_stats('m')

# Fetch statistics for women's playoff teams
women_team_stats_df = usport_teams_stats('w', 'playoffs')

# Fetch statistics for women's players playing in U Sports championship Final 8
women_player_stats_df = usport_players_stats('w', 'championship')
```

- ### Viewing Column Names

```python
# Use these code snippets to see all column names in each DataFrame
# For the team statistics DataFrame
print("Column names in men's player statistics DataFrame:")
print(men_player_stats_df.columns.tolist())

# For the player statistics DataFrame
print("\nColumn names in men's player statistics DataFrame:")
print(men_player_stats_df.columns.tolist())
```


- ### Exporting DataFrame to different files

```python
# Export the  to a CSV file using the `to_csv()` method
men_team_stats_df.to_csv('men_team_stats.csv', index=False)  # Export without row index

#Export to a HTML table representation using to_html method
men_team_stats_df.to_html('table.html')

#Export to a JSON file using the to_json() method
men_team_stats_df.to_json('men_team_stats.json', orient='records') # Export in 'records' format

#Export to a SQLite database using the to_sql() method (requires SQLAlchemy)
from sqlalchemy import create_engine

engine = create_engine('sqlite:///usports_stats.db') #Export to SQLite database
women_team_stats_df.to_sql('team_stats', con=engine, index=False) # Export without row index
women_player_stats_df.to_sql('player_stats', con=engine, index=False) # Export without row index
```

### Explore [Pandas DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) documentation for instructions on manipulating data and performing data analysis.

## Author

This package was developed by OJ Adeyemi.

## Contributing

Contributions, bug reports, and feature requests are welcome! Please feel free to open an issue or submit a pull request on [GitHub](https://github.com/ojadeyemi/usports-basketball).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
for details.
