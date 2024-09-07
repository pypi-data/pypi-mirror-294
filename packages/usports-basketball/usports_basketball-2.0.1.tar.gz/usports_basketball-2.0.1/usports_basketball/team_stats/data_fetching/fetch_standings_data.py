import asyncio
from typing import Any

from bs4 import BeautifulSoup, Tag
from playwright.async_api import async_playwright

from ...utils import clean_text, get_random_header
from ..team_settings import standings_type_mapping
from .fetch_team_stats import merge_team_data


def parse_standings_table(soup: BeautifulSoup, columns: list[str]) -> list[dict[str, Any]]:
    """Parse standings data from an HTML table"""
    table_data: list[dict[str, Any]] = []

    # Find all rows in the table
    rows: list[Tag] = soup.find_all("tr")

    for row in rows:
        row_data = {}

        # Extract the team name from the <th> element
        team_name_th = row.find("th", class_="team-name")
        if team_name_th:
            team_name_tag = team_name_th.find("a")
            if team_name_tag:
                team_name = clean_text(team_name_tag.get_text())
                row_data["team_name"] = team_name

        # Extract the column data from <td> elements
        cols: list[Tag] = row.find_all("td")
        if cols:
            for col, column_name in zip(cols, columns):
                row_data[column_name] = clean_text(col.get_text())

            table_data.append(row_data)

    return table_data


async def fetching_standings_data(standings_url: str) -> list[dict[str, Any]]:
    """function for handling fetch standings data from standings url"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, timeout=10000)
        page = await browser.new_page()

        headers = get_random_header()
        await page.set_extra_http_headers(headers)
        # Block unnecessary resources
        await page.route(
            "**/*.{png,jpg,jpeg,gif,webp,css,woff2,woff,js}",
            lambda route: route.abort(),
        )

        await page.goto(standings_url, timeout=10000)

        await page.wait_for_selector("tbody", timeout=10000)
        tables = await page.query_selector_all("tbody")

        tables_length = len(tables)

        all_standings = []
        all_team_records = []
        for i in range(0, tables_length):
            table = await tables[i].inner_html()

            standings_html = table.replace("\n", "").replace("\t", "")

            soup = BeautifulSoup(standings_html, "html.parser")

            column_names = list(standings_type_mapping.keys())[1:]
            standings_data = parse_standings_table(soup, column_names)
            team_record_data = await fetch_team_record_data(soup)

            all_standings = merge_team_data(all_standings, standings_data)
            all_team_records = merge_team_data(all_team_records, team_record_data)

        await browser.close()

        return all_standings, all_team_records


async def fetch_team_record_data(soup: BeautifulSoup) -> list[dict[str, str]]:
    """Fetch data for all teams based on the provided soup."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, timeout=5000)

        # Extract all team <a> tags from the standings page
        team_name_tags = soup.find_all("a", href=True)

        # Fetch all team records concurrently
        async def fetch_team_record(team_name_tag: Tag) -> dict[str, str]:
            page = await browser.new_page()
            headers = get_random_header()
            await page.set_extra_http_headers(headers)

            # Block unnecessary resources to speed up page load
            await page.route("**/*.{png,jpg,jpeg,gif,webp,css,woff2,woff,js}", lambda route: route.abort())

            href = team_name_tag.get("href")
            team_name = clean_text(team_name_tag.get_text(strip=True))
            team_url = f"https://universitysport.prestosports.com{href}"

            await page.goto(team_url, wait_until="networkidle")

            # Extract the <ul> tag with the class name 'team-stats'
            ul_content = await page.locator("ul.team-stats").inner_html()

            # Parse the HTML with BeautifulSoup
            team_soup = BeautifulSoup(ul_content, "html.parser")

            stats = {"team_name": team_name}

            # Mapping categories to dictionary keys
            category_mapping = {"Streak": "streak", "Home": "home", "Away": "away"}

            # Loop through each <li> tag and extract the relevant data

            li: Tag
            for li in team_soup.find_all("li"):
                category_div = li.find("div", class_=lambda c: c and "small text-uppercase" in c)
                if category_div:
                    category = category_div.get_text(strip=True)
                    if category in category_mapping:
                        value_div = li.find("div", class_="fs-4 lh-1 text-nowrap fw-bold")
                        value = value_div.get_text(strip=True) if value_div else None
                        stats[category_mapping[category]] = value

            await page.close()
            return stats

        # Create tasks for each team to fetch data concurrently
        tasks = [fetch_team_record(tag) for tag in team_name_tags]

        # Run all tasks concurrently and gather the results
        all_team_data = await asyncio.gather(*tasks)

        await browser.close()

    return all_team_data
