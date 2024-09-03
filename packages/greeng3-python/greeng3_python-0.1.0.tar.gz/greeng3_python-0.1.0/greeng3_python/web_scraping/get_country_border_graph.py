#!/usr/bin/env python3

import json
import os

import requests
from bs4 import BeautifulSoup

URL = 'https://en.wikipedia.org/wiki/List_of_countries_and_territories_by_land_borders'
CACHED_PATH = 'List_of_countries_and_territories_by_land_borders.html'
OUTPUT_PATH = 'country_border_graph.json'


def cached_or_fetched():
    if not os.path.isfile(CACHED_PATH):
        response = requests.get(URL, stream=True)
        if response.status_code < 400:
            with open(CACHED_PATH, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)

    with open(CACHED_PATH, "rb") as f:
        return f.read()


def country_border_graph():
    as_json = {}
    page = cached_or_fetched()
    soup = BeautifulSoup(page, 'html.parser')
    data_table = soup.find_all("table", class_="wikitable sortable")[0]
    rows = data_table.find_all('tr')
    for row in rows:
        columns = row.find_all('td')

        if len(columns) == 0:
            # headers, or whatever
            continue

        src_country = columns[0].find('a').text
        dst_countries = [flag.next_sibling.text for flag in
                         columns[5].find_all("span", class_="flagicon") if flag.next_sibling]

        as_json[src_country] = dst_countries
    return as_json


def main():
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(country_border_graph(), f, indent=2, sort_keys=True, separators=(', ', ': '))


if __name__ == "__main__":
    main()
