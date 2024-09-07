from typing import Any

from bs4 import BeautifulSoup, Tag
from playwright.async_api import async_playwright

from ...utils import clean_text, fetch_table_html, get_random_header, split_made_attempted
from ..team_settings import stat_group_options, team_stats_columns_type_mapping


def merge_team_data(existing_data: list[dict[str, Any]], new_data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Merge existing and new team data stats"""
    data_dict = {f"{item['team_name']}": item for item in existing_data}

    for new_item in new_data:
        key = f"{new_item['team_name']}"
        if key in data_dict:
            data_dict[key].update(new_item)
        else:
            data_dict[key] = new_item

    return list(data_dict.values())


def parse_team_stats_table(soup: BeautifulSoup, columns: list[str]) -> list[dict[str, Any]]:
    """Parse team stats data from an HTML table"""
    table_data: list[dict[str, Any]] = []
    rows: list[Tag] = soup.find_all("tr")

    for row in rows:
        cols: list[Tag] = row.find_all("td")
        if len(cols) > 1:
            row_data = {}
            team_name = clean_text(cols[1].get_text())
            games_played = clean_text(cols[2].get_text())
            row_data["team_name"] = team_name
            row_data["games_played"] = games_played
            for j, col in enumerate(columns):
                if j < len(cols) - 1:
                    value = cols[j + 3].get_text().strip()
                    if col in [
                        "field_goal_made",
                        "three_pointers_made",
                        "free_throws_made",
                        "field_goal_made_against",
                        "three_pointers_made_against",
                    ]:
                        made, attempted = split_made_attempted(value)
                        row_data[col] = made
                        row_data[col.replace("made", "attempted")] = attempted
                    else:
                        row_data[col] = value
            table_data.append(row_data)

    return table_data


async def fetching_team_stats(stats_url: str):
    """function for handling fetching team stats from url"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, timeout=10000)
        page = await browser.new_page()

        headers = get_random_header()
        await page.set_extra_http_headers(headers)

        # Block unnecessary resources to speed up page load
        await page.route("**/*.{png,jpg,jpeg,gif,webp,css,woff2,woff,js}", lambda route: route.abort())

        try:
            await page.goto(stats_url, timeout=60 * 1000)
            all_data = []
            team_table_names = stat_group_options.keys()
            for index, _ in enumerate(team_table_names):
                table_html = await fetch_table_html(page, index)

                soup = BeautifulSoup(table_html, "html.parser")
                columns = team_stats_columns_type_mapping[index]
                column_names = list(columns.keys())
                table_data = parse_team_stats_table(soup, column_names)
                all_data = merge_team_data(all_data, table_data)

            return all_data
        except Exception as e:
            raise RuntimeError(f"Error fetching team stats: {e}") from e
        finally:
            await browser.close()
