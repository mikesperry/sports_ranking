
import urllib.request as _urlr
from bs4 import BeautifulSoup as _bs4


def cleanhtml(url):
    """
    A methond to parse and deal with regular html pages

    Args:
        url: the url to be parsed

    Returns:
        bsoup: a BeautifulSoup object with the pages contents
    """
    html = _urlr.urlopen(url).read()
    bsoup = _bs4(html, "lxml")
    # kill all script and style elements
    for script in bsoup(["style"], ["script"]):
        script.extract()    # rip it out
    return bsoup


def is_abbrev(abbrev, text):
    abbrev = abbrev.lower()
    text = text.lower()
    if not abbrev:
        return True
    if abbrev and not text:
        return False
    if abbrev[0] == 'u' and len(abbrev) > 1:
        if text[0] != 'u':
            abbrev = abbrev[1:]
    if len(abbrev) > 4:
        abbrev = abbrev[:4]
    words = text.split()
    if abbrev[0] != text[0]:
        return False
    else:
        return (is_abbrev(abbrev[1:], ' '.join(words[1:])) or
                any(is_abbrev(abbrev[1:], text[i+1:])
                    for i in range(len(words[0]))))
