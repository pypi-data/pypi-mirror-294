import os
from collections import defaultdict
from pprint import PrettyPrinter

from ..isbn.isbn import isbn_find_raw

pp = PrettyPrinter(indent=4)


def relevant_dict(d):
    """
    Return a copy of a dict without any key that had an empty value

    :param d: dict in which some keys' values maybe be empty
    :return: dict with only keys that have non-empty values
    """
    relevant = {}
    for k, v in d.iteritems():
        if v:
            relevant[k] = v
    return relevant


def attempt_gs(path):
    # cmd = 'gs -dNODISPLAY -dSAFER -dDELAYBIND -dWRITESYSTEMDICT -dSIMPLE -dQUIET -f ps2ascii.ps "%s" -c quit' % path
    # TODO
    pass


def attempt_pypdf2(path, fields):
    """
    PyPDF2 style
    sudo pip install pypdf2

    :param path: pathname of a PDF file
    :param fields: counter of populated fields
    :return: dict of metadata found
        {
            "author": string, # free form author(s) - from /Author
            "identifier": string # ISBN or the like
            "keywords": string # free form keyword(s) - from /Keywords, which can be iffy
            "subject": string # free form subject - from /Subject, which can be iffy
            "title": string # title - from /[Tt]itle, which is occasionally worthless
        }
    """
    metadata_dict = {}
    from PyPDF2 import PdfFileReader
    from PyPDF2.utils import PdfReadError
    with open(path, 'rb') as f:
        try:
            pdf_file = PdfFileReader(f)
            info = pdf_file.getDocumentInfo()
            if info:
                info = relevant_dict(dict(info))

                if '/Author' in info:
                    metadata_dict['author'] = info['/Author']

                if '/Keywords' in info:
                    metadata_dict['keywords'] = info['/Keywords']

                if '/Subject' in info:
                    metadata_dict['subject'] = info['/Subject']

                if '/Title' in info:
                    metadata_dict['title'] = info['/Title']
                elif '/title' in info:
                    metadata_dict['title'] = info['/title']

                for k, v in info.iteritems():
                    if v:
                        fields[k].append(v)
            meta = pdf_file.getXmpMetadata()
            if meta:
                dc_subject = ' '.join(meta.dc_subject)
                if dc_subject:
                    fields['dc_subject'].append(dc_subject)
                    if 'subject' in metadata_dict:
                        metadata_dict['dc_subject'] = dc_subject
                    else:
                        metadata_dict['subject'] = dc_subject

                dc_title = meta.dc_title
                if dc_title:
                    if 'x-default' in dc_title and dc_title['x-default']:
                        if 'title' in metadata_dict:
                            metadata_dict['dc_title'] = dc_title['x-default']
                        else:
                            metadata_dict['title'] = dc_title['x-default']
                        fields['dc_title'].append(dc_title['x-default'])

                pdf_keywords = meta.pdf_keywords
                if pdf_keywords:
                    fields['pdf_keywords'].append(pdf_keywords)
                    if 'keywords' in metadata_dict:
                        metadata_dict['pdf_keywords'] = pdf_keywords
                    else:
                        metadata_dict['keywords'] = pdf_keywords
        except PdfReadError as e:
            print('    PdfReadError: {e}')

    best_isbn = isbn_find_raw(os.path.basename(path))
    for k, v in metadata_dict.iteritems():
        if not isinstance(v, str):
            print(type(v))
            print(v.__dict__)
            print(str(dict))
        isbn = isbn_find_raw(v)
        if len(isbn) > len(best_isbn):
            best_isbn = isbn
    if best_isbn:
        metadata_dict['isbn'] = best_isbn
    return metadata_dict


if __name__ == '__main__':
    home = os.environ['HOME']
    test_root = os.path.join(home, 'Google Drive/Books, Papers')
    metadata_by_file = {}
    populated_fields = defaultdict(list)

    for n in os.listdir(test_root):
        pn = os.path.join(test_root, n)
        if os.path.isdir(pn) or not n.lower().endswith('.pdf'):
            continue
        print('{n}:')
        metadata = attempt_pypdf2(pn, populated_fields)
        metadata_by_file[pn] = metadata
        pp.pprint(metadata)
        print('-----------------')
