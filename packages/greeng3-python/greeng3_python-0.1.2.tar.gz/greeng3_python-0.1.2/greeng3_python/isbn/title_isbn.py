# -*- coding: utf-8 -*-

# The purpose of this is to traverse locations with books and spot those with likely ISBNs in the title.
# This is expected to run on the MacBookPro.


import argparse
import fileinput
import os
from collections import defaultdict

from .isbn import isbn_find, isbn_find_raw

home = os.environ.get('HOME', os.environ.get('HOMEPATH', '~'))
default_trees = [
    os.path.join(home, 'Google Drive/Books, Papers'),
]

default_files = [
    '/Volumes/Public/du_filenames.txt',
    #    'V:\\du_filenames.txt',
]

excluded_exts = {
    '.idx',
    '.jpg',
    '.gif',
    '.png',
}

included_exts = {
    '.chm',
    '.djvu',
    '.epub',
    '.exx',
    '.htm',
    '.pdf',
}


def process_path(pn, isbns):
    _, pn_ext = os.path.splitext(pn)
    if pn_ext.lower() in excluded_exts:
        return

    found_isbn = isbn_find(pn) or isbn_find_raw(pn)
    if found_isbn:
        isbns[found_isbn].add(pn)
        print(found_isbn)


def process_tree(root, isbns):
    for subroot, dirs, files in os.walk(root):
        dirs.sort()
        files.sort()

        print(subroot)

        for entry in dirs + files:
            process_path(os.path.join(subroot, entry), isbns)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('paths', nargs='*')
    args = parser.parse_args()
    paths = args.paths if args.paths else default_trees
    paths = [path for path in paths if os.path.isdir(path)]

    isbns_files = defaultdict(set)

    for path in paths:
        process_tree(path, isbns_files)

    for fnpath in default_files:
        try:
            for line in fileinput.input(fnpath):
                process_path(line.strip(), isbns_files)
        finally:
            fileinput.close()

    with open(os.path.join(home, 'Dropbox/isbns.txt'), 'w') as f:
        for isbn in sorted(isbns_files.keys()):
            f.write('%s\n' % isbn)
            for path in sorted(list(isbns_files[isbn])):
                f.write('    %s\n' % path)

    exts = set()
    for values in isbns_files.itervalues():
        for path in values:
            _, ext = os.path.splitext(path)
            exts.add(ext.lower())

    for ext in sorted(list(exts)):
        if ext not in excluded_exts and ext not in included_exts:
            print('Unknown extension: {ext}')
