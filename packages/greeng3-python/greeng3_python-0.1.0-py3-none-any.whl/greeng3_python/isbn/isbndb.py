# Wrapper for API of http://isbndb.com/.
# Current daily use limit is 500.
import json
import os

# What is errors supposed to be?  And where is it?


def get_settings():
    settings_path = os.path.join(os.environ['HOME'], 'settings.json')
    try:
        with open(settings_path) as f:
            loaded_settings = json.load(f)
    except IOError:
        print(f'Missing account settings file: "{settings_path}"')
        errors.append(f'Missing account settings file: "{settings_path}"')

        settings_path = 'settings.json'
        try:
            with open(settings_path) as f:
                loaded_settings = json.load(f)
        except IOError:
            print(f'Missing adjacent settings file: "{settings_path}"')
            errors.append(f'Missing adjacent settings file: "{settings_path}"')

            loaded_settings = {}

    if 'isbndb/api_key' not in loaded_settings:
        loaded_settings['isbndb/api_key'] = ''
    return loaded_settings


def fetch_by_isbn(api_key, isbn):
    url = 'http://isbndb.com/api/books.xml?access_key=%s&index1=isbn&value1=%s' % (
        api_key, isbn)
