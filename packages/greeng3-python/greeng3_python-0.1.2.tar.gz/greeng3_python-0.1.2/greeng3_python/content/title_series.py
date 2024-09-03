import fileinput
import os
import re
from collections import defaultdict

from ..isbn.isbn import isbn_find, isbn_find_raw, isbn_cmp

# base_path = '/Volumes/Public'
base_path = '/Users/greeng3/Dropbox/Inventories'
# base_path = 'c:/Users/Gordon Greene/Dropbox/Inventories'
filenames_pn = os.path.join(base_path, 'du_filenames.txt')
series_pn = os.path.join(base_path, 'series.csv')
series_strs_pn = os.path.join(base_path, 'series_strs.csv')

# series: number: isbn, [filenames]
# Cambridge Tracts in Theoretical Computer Science
# European Association for Theoretical Computer Science

series_known = {
    'CSLI',
    'GTM',
    'LNAI',
    'LNCS',
    'LNL',
    'LNM',
    'LNPAM',
    'UTM',
}

series_details = [
    ['LNCS', [
        re.compile(
            r'(lecture\s+notes(?:\s+in)?\s+computer\s+science)\s*(\d+)', re.I),
    ]],
    ['LNM', [
        re.compile(r'(lecture\s+notes(?:\s+in)?\s+mathematics)\s*(\d+)', re.I),
    ]],
    ['LNL', [
        re.compile(r'(lecture\s+notes(?:\s+in)?\s+logic)\s*(\d+)', re.I),
    ]],
    ['LNAI', [
        re.compile(
            r'(lecture\s+notes(?:\s+in)?\s+artificial\s+intelligence)\s*(\d+)', re.I),
    ]],
    ['LNPAM', [
        re.compile(
            r'(lecture\s+notes(?:\s+in)?\s+pure(?:\s+and)?\s+applied\s+mathematics)\s*(\d+)', re.I),
    ]],
    ['CSLI', [
        re.compile(r'(center(?:\s+for)?(?:\s+the)?\s+study(?:\s+of)?\s+language(?:\s+and)?\s+information)\s*(\d+)',
                   re.I),
    ]],
    ['UTM', [
        re.compile(
            r'(undergraduate\s+text(?:\s+in)?\s+mathematics)\s*(\d+)', re.I),
    ]],
    ['GTM', [
        re.compile(r'(graduate\s+text(?:\s+in)?\s+mathematics)\s*(\d+)', re.I),
    ]],
    ['', [
        re.compile(r'\[([a-z]+)\]\s*(\d+)', re.I),  # [LNCS] 10
        re.compile(r'\[([a-z]+)\s*(\d+)\]', re.I),  # [LNCS 10]
        re.compile(r'\[([a-z]+)\]\s*\[(\d+)\]', re.I),  # [LNCS][10]
        re.compile(r'\(([a-z]+)\)\s*(\d+)', re.I),  # (LNCS) 10
        re.compile(r'\(([a-z]+)\s*(\d+)\)', re.I),  # (LNCS 10)
        re.compile(r'\(([a-z]+)\)\s*\((\d+)\)', re.I),  # (LNCS)(10)
        re.compile(r'([a-z]+)\s*(\d+)', re.I),  # LNCS 10, LNCS10
    ]],
]

series_yes = {
    'LNCS', 'LNM', 'LNPAM', 'LNL', 'UTM', 'MTCS', 'MPLS', 'LNB', 'PCS',
}

if __name__ == '__main__':
    books = defaultdict(set)
    series_strs = defaultdict(int)
    try:
        for line in fileinput.input(filenames_pn):
            line = line.strip()

            for series in series_details:
                m = None
                for regex in series[1]:
                    m = regex.search(line)
                    if m:
                        break
                if m:
                    series_str = series[0] or m.group(1).upper()
                    series_num = int(m.group(2))
                    book_id = series_str, series_num
                    found_isbn = isbn_find(line) or isbn_find_raw(line)
                    books[book_id].add(found_isbn)
                    print(f'{series_str} {series_num} {found_isbn}')
                    break
    finally:
        fileinput.close()

    with open(series_pn, 'w') as outfile:
        for book_id in sorted(books.keys()):
            series_str = book_id[0]
            series_strs[series_str] += 1
            if series_str in series_yes:
                isbns = [isbn for isbn in sorted(
                    list(books[book_id]), cmp=isbn_cmp) if isbn]
                # book_id is a tuple?
                row = ','.join(['"%s",%d' % book_id] + isbns)
                outfile.write(row + '\n')

    with open(series_strs_pn, 'w') as outfile:
        for item in sorted(series_strs.items(), cmp=lambda x, y: cmp(x[1], y[1]) or cmp(x[0], y[0])):
            outfile.write('"%s",%d\n' % item)
            if book_id[0] in series_known:
                isbns = [isbn for isbn in sorted(
                    list(books[book_id]), cmp=isbn_cmp) if isbn]
                # book_id is a tuple?
                row = ','.join(['"%s",%d' % book_id] + isbns)
                outfile.write(row + '\n')
