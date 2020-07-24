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
    return title.strip()


def article_action(article, cat, article_name):
    address = 'https://bankreferatov.kz' + BeautifulSoup.find(article, 'a')['href']
    article_name = format_title(article_name)
    print('Parsing ' + address + ' ...')
    try:
        adr = open(os.path.join(cat, article_name.replace('\"', "").replace("\'", "").replace("«", "").replace("»", ""))
                   + '.url', 'w', encoding='utf-8')
        adr.write(address)
        adr.close()

        req2 = urllib.request.urlopen(address)
        html2 = req2.read()
        soap2 = BeautifulSoup(html2, 'html.parser')
        text = soap2.find('div', class_='article-content').get_text(strip=True)
        text = format_sentence(text)
        print(article_name)
        f = open(os.path.join(cat, article_name.replace('\"', "").replace("\'", "").replace("«", "").replace("»", ""))
                 + '.txt', 'w', encoding='utf-8')
        f.write(text)
        f.close()
    except:
        pass


