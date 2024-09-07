import asyncio
from typing import Any

from bs4 import BeautifulSoup, Tag
from playwright.async_api import Page, async_playwright

from ...utils import clean_text, fetch_table_html, get_random_header, split_made_attempted
from ..player_settings import player_stats_columns_type_mapping


def parse_player_stats_table(soup: BeautifulSoup, columns: list[str]) -> list[dict[str, Any]]:
    """Parse player stats data from an HTML table."""
    table_data: list[dict[str, Any]] = []
    rows: list[Tag] = soup.find_all("tr")

    for row in rows:
        cols: list[Tag] = row.find_all("td")
        if len(cols) > 1:
            row_data = {}
            player_name = clean_text(cols[1].get_text())
            school = clean_text(cols[2].get_text())
            games_played = clean_text(cols[3].get_text())
            games_started = clean_text(cols[4].get_text())
            row_data["player_name"] = player_name
            row_data["school"] = school
            row_data["games_played"] = games_played
            row_data["games_started"] = games_started
            for j, col in enumerate(columns):
                if j < len(cols) - 1:
                    value = cols[j + 5].get_text().strip()
                    if col in [
                        "field_goal_made",
                        "three_pointers_made",
                        "free_throws_made",
                    ]:
                        made, attempted = split_made_attempted(value)
                        row_data[col] = made
                        row_data[col.replace("made", "attempted")] = attempted
                    else:
                        row_data[col] = value
        table_data.append(row_data)

    return table_data


def merge_player_data(existing_data: list[dict[str, Any]], new_data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Merge existing and new player data stats."""
    data_dict = {f"{item['player_name']}_{item['school']}_{item['games_played']}": item for item in existing_data}

    for new_item in new_data:
        key = f"{new_item['player_name']}_{new_item['school']}_{new_item['games_played']}"
        if key in data_dict:
            data_dict[key].update(new_item)
        else:
            data_dict[key] = new_item

    return list(data_dict.values())


async def fetch_table_data(page: Page, index: int, columns: dict[str, type]):
    """Fetch and parse a specific table from the page."""
    table_html = await fetch_table_html(page, index)
    soup = BeautifulSoup(table_html, "html.parser")
    column_names = list(columns.keys())
    return parse_player_stats_table(soup, column_names)


async def fetching_player_stats(url: str):
    """Function for handling fetching data from players stat url"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, timeout=10000)
        page = await browser.new_page()
        headers = get_random_header()
        await page.set_extra_http_headers(headers)

        # Block unnecessary resources to speed up page load
        await page.route("**/*.{png,jpg,jpeg,gif,webp,css,woff2,woff,js}", lambda route: route.abort())

        try:
            await page.goto(url, timeout=50000)
            tasks = [fetch_table_data(page, index + 3, player_stats_columns_type_mapping[index]) for index in range(3)]

            results = await asyncio.gather(*tasks)

            all_data = []
            for result in results:
                all_data = merge_player_data(all_data, result)

            return all_data

        except Exception as e:
            raise RuntimeError(f"Error fetching team stats: {e}") from e
        finally:
            await browser.close()
