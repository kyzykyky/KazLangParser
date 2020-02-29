import urllib.request
from bs4 import BeautifulSoup


def format_sentence(sentence):
    sentence = sentence.split(". ")
    lines = ''
    for s in sentence:
        lines += s + "\n"
    return lines.strip()