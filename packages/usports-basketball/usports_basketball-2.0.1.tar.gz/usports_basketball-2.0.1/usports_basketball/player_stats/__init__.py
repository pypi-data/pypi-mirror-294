"""
Module for fetching and processing U Sports basketball player statistics.

This module provides a function to retrieve and combine player statistics
from the U Sports basketball league for both men's and women's teams.
It utilizes web scraping techniques to extract data from the U Sports website
and processes it into pandas DataFrames for further analysis.

Function:
- usport_players_stats: Fetch and combine current player statistics.

Author:
    OJ Adeyemi

Date Created:
    August 6, 2024
"""

import asyncio
import logging
import random

from pandas import DataFrame, concat
from pandas.errors import EmptyDataError

from ..utils import get_sport_identifier, setup_logging
from .data_processing import get_players_stats_df
from .player_settings import sort_categories

SEASON_URLS = {"regular": "2023-24", "playoffs": "2023-24p", "championship": "2023-24c"}
BASE_URL = "https://universitysport.prestosports.com/sports"

setup_logging()
logger = logging.getLogger(__name__)


def __construct_urls(gender: str, season_option: str) -> str:
    sport = get_sport_identifier(gender)
    try:
        base_url = SEASON_URLS[season_option]
    except KeyError as e:
        available_options = ", ".join(SEASON_URLS.keys())
        raise ValueError(f"Invalid season option {season_option}. Available options: {available_options}") from e

    player_stats_url = f"{BASE_URL}/{sport}/{base_url}/players?pos=sh&r=0&sort={{sort_category}}"
    return player_stats_url


def __construct_player_urls(gender: str, season_option: str) -> list[str]:
    player_stats_url_template = __construct_urls(gender, season_option)

    urls = []
    for sort_category in sort_categories:
        url = player_stats_url_template.format(sort_category=sort_category)
        urls.append(url)

    return urls


async def __fetch_with_delay(url: str) -> DataFrame:
    await asyncio.sleep(random.uniform(0.5, 2.0))
    logger.debug(f"Fetching stats on category: {url[-5:]}")
    players_df = await get_players_stats_df(url)
    return players_df


async def __fetch_and_merge_player_stats(urls: list[str]) -> DataFrame:
    all_dataframes = []

    batch_size = 10
    num_of_urls = len(urls)

    for i in range(0, num_of_urls, batch_size):
        logger.debug(f"GETTING BATCH {i+1} - {i+batch_size} out of {num_of_urls}")
        batch_urls = urls[i : i + batch_size]
        tasks = [__fetch_with_delay(url) for url in batch_urls]
        dataframes = await asyncio.gather(*tasks)
        all_dataframes.extend(dataframes)

    if not all_dataframes:
        raise EmptyDataError("No data received, all DataFrames are empty")

    merged_df = concat(all_dataframes, ignore_index=True).drop_duplicates().reset_index(drop=True)

    return merged_df


def usport_players_stats(arg: str, season_option: str = "regular") -> DataFrame:
    """
    Fetch and process player statistics data from the USports website.

    Args:
        arg (str): Gender of the players. Accepts 'men', 'women', 'm', or 'w' (case insensitive).
        season_option (str): The season option to fetch data for. Options are:
            - 'regular': Regular season statistics (default).
            - 'playoffs': Playoff season statistics.
            - 'championship': Championship season statistics.

    Returns:
        DataFrame: DataFrame containing processed player statistics.
    """
    # Normalize and map the input argument
    arg = arg.lower()
    if arg in ["m", "men"]:
        gender = "men"
    elif arg in ["w", "women"]:
        gender = "women"
    else:
        raise ValueError("The argument 'arg' should be either 'men', 'm', 'w', or 'women'")

    logger.info(f"FETCHING {gender.upper()} {season_option.upper()} SEASON PLAYERS STATS")
    urls = __construct_player_urls(gender, season_option)

    df = asyncio.run(__fetch_and_merge_player_stats(urls))
    return df
