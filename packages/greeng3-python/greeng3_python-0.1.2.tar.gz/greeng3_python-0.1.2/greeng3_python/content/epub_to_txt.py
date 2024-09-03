from bs4 import BeautifulSoup
import ebooklib
from ebooklib import epub
import re
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters

blacklist = ['[document]',   'noscript', 'header',
             'html', 'meta', 'head', 'input', 'script', ]
# there may be more elements you don't want, such as "style", etc.


def epub2thtml(epub_path):
    book = epub.read_epub(epub_path)
    chapters = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            chapters.append(item.get_content())
    return chapters


def chap2text(chap):
    output = ''
    soup = BeautifulSoup(chap, 'html.parser')
    text = soup.find_all(text=True)
    for t in text:
        if t.parent.name not in blacklist:
            output += f'{t} '
    return output


def thtml2ttext(thtml):
    Output = []
    for html in thtml:
        text = chap2text(html)
        Output.append(text)
    return Output


def epub2text(epub_path):
    chapters = epub2thtml(epub_path)
    ttext = thtml2ttext(chapters)
    return ttext


if __name__ == '__main__':
    out = epub2text(
        'inputs/Midnight at the Well of Souls - Jack L. Chalker.epub')
    punkt_param = PunktParameters()
    sentence_splitter = PunktSentenceTokenizer(punkt_param)

    lines = []
    for block in out:
        for chunk in [bit.strip() for bit in block.split('\n') if bit.strip()]:
            sentences = sentence_splitter.tokenize(chunk)
            lines += sentences

    blocksize = 0
    with open('inputs/midnight_at_the_well_of_souls.txt', 'w') as f:
        for txt in lines:
            increment = len(txt) + 1
            if blocksize + increment > 15000:
                f.write('--------------\n')
                blocksize = 0
            f.write(txt)
            f.write('\n')
            blocksize += increment
