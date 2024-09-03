#!/usr/bin/env python3

import json
import os

import requests
from bs4 import BeautifulSoup

URL = 'https://en.wikipedia.org/wiki/List_of_national_capitals_by_population'
CACHED_PATH = 'List_of_national_capitals_by_population.html'
OUTPUT_PATH = 'national_capitals.json'


def cached_or_fetched():
    if not os.path.isfile(CACHED_PATH):
        response = requests.get(URL, stream=True)
        if response.status_code < 400:
            with open(CACHED_PATH, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)

    with open(CACHED_PATH, 'rb') as f:
        return f.read()


def country_capitals():
    as_json = {}
    page = cached_or_fetched()
    soup = BeautifulSoup(page, 'html.parser')
    data_table = soup.find_all('table')[1]
    rows = data_table.find_all('tr')
    for row in rows:
        country_column = row.find('th')
        columns = row.find_all('td')

        if len(columns) == 0:
            # headers, or whatever
            continue

        country = country_column.text.strip().replace(' *', '')
        capital = columns[0].find('a').text
        as_json[country] = capital

    # TODO post processing step to trim country names in parentheses and embedded stars and nbsp

    return as_json


def main():
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(country_capitals(), f, indent=2,
                  sort_keys=True, separators=(', ', ': '))


if __name__ == '__main__':
    main()
