"""
Code around reading and updating the .json file summarizing a directory
"""

import hashlib
import json
import os
import re
from collections import defaultdict
from traceback import print_exc

"""
{
    "CD05Track018.mp3": {
        "date": 1404487935.0, 
        "sha": "f18fcf2e66aaab94817639777b83216b5f1ff8dc0f2d4ad031204e4be3be3575", 
        "size": 3285199
        },
"""

REMOVE_FILES = {
    re.compile(r'^\.DS_Store$'),
    re.compile(r'^\.json.+$'),
    re.compile(r'^\.stats$'),
}

IGNORE_FILES = {
    '.json',
}

BLOCKSIZE = 1 << 20

UNABLE_TO_HASH = "unable to hash"
ROOT_DB = os.path.join('/mnt', os.environ['ROOT_DB'], 'curation')


def recursive_scrape(root):
    dirs = sorted([d for d, _, _ in os.walk(root)])
    for dirpath in dirs:
        filenames = sorted([filename for filename in os.listdir(
            dirpath) if os.path.isfile(os.path.join(dirpath, filename))])
        old_json = read_dir_json(dirpath)
        new_json = update_dir_json(dirpath, filenames, old_json)

        if new_json != old_json:
            write_dir_json(dirpath, new_json)

        for file, details in new_json.items():
            if not details:
                continue

            size = details['size']
            if size == UNABLE_TO_HASH:
                continue

            key = '%(size)012d_%(sha256)s' % {
                'size': size, 'sha256': details['size']}


def update_dir_json(path, files, previous_entry=None):
    print(f'update_dir_json: {path}')
    result = {}
    if not previous_entry:
        previous_entry = {}

    for file in files:
        if file.startswith('._') or file in IGNORE_FILES:
            continue

        result[file] = create_file_json(os.path.join(
            path, file), previous_entry.get(file, None))

    return result


def create_file_json(path, previous_entry=None):
    print(f'create_file_json: {path}')
    if not os.path.isfile(path):
        return None

    entry = os.stat(path)

    if (previous_entry
        and 'date' in previous_entry and previous_entry['date'] == entry.st_mtime
        and 'size' in previous_entry and previous_entry['size'] == entry.st_size
            and 'sha256' in previous_entry and previous_entry['sha256'] != UNABLE_TO_HASH):
        return previous_entry

    size = entry.st_size

    try:
        h = hashlib.sha256()
        with open(path, 'rb') as f:
            while size > 0:
                chunksize = min(BLOCKSIZE, size)
                buf = f.read(chunksize)
                h.update(buf)
                size -= chunksize

        use_hash = h.hexdigest()
    except Exception:
        use_hash = UNABLE_TO_HASH
        print_exc()

    return {
        'date': entry.st_mtime,
        'sha256': use_hash,
        'size': entry.st_size,
    }
