import urllib.request
from bs4 import BeautifulSoup
import os
import re


def format_sentence(sentence):
    sentence = sentence.split(". ")
    lines = ''
    for s in sentence:
        lines += s + ".\n"
    return lines.strip()


def format_title(title):
    title = re.sub(r"\d+", "", title)
    return title.strip().replace('\"', "").replace("\'", "").replace("«", "").replace("»", "")


def clean_me(html):
    soup = BeautifulSoup(html)
    for s in soup(['script', 'style']):
        s.decompose()
    return ' '.join(soup.stripped_strings)


def article_action(article, cat, article_name):
    try:
        href = BeautifulSoup.find(article, 'a')['href']
        try:
            adr = open(os.path.join(cat, format_title(article_name)) + '.url', 'w', encoding='utf-8')
            adr.write(href)
            adr.close()
        except:
            pass
        print('Parsing ' + href + ' ...')
        req2 = urllib.request.urlopen(href)
        html2 = req2.read()
        soap2 = BeautifulSoup(html2, 'html.parser')
        [s.extract() for s in soap2('script')]
        text = soap2.find('div', class_='entry-inner').get_text(strip=True)
        text = format_sentence(text)
        f = open(os.path.join(cat, format_title(article_name)) + '.txt', 'w', encoding='utf-8')
        f.write(text)
        f.close()
    except:
        pass

