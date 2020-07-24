from bs4 import BeautifulSoup
import urllib.request
import  urllib.error
from urllib.request import urlopen
import os
import re


# for a in soap.find_all('a', href=True):          Все Href'ы
#   print("Found the URL:", a['href'])


# with urlopen(page) as url:      Пайтон 3 откр ЮРЛ
#     s = url.read()
base = 'https://articlekz.com'


def format_sentence(sentence):
    sentence = sentence.split(". ")
    lines = ''
    for s in sentence:
        lines += s + ".\n"
    return lines.strip()


def format_title(title):
    title = re.sub(r"\d+", "", title)
    return title.strip()


def my_url_open(page):
    with urlopen(page) as url:
        s = url.read()
    return s


def parse_article_kz_com(url, cat):
    BASE_SITE = url
    req = urllib.request.urlopen(BASE_SITE)
    html = req.read()

    art_count = 0  # 1111

    if not os.path.exists(cat):
        os.mkdir(cat)

    soap = BeautifulSoup(html, 'html.parser')
    page_count = soap.find_all('li', class_='page-item')[-2].get_text(strip=True)
    current_page = 1
    print('Category ' + cat + ' has ' + page_count + ' pages.\n')

    for x in range(1, int(page_count) + 1):
        links = {}
        print('Parsing page №', current_page)
        for article in soap.find_all('h1', class_='card-title h5'):
            for a in article:
                links[a['href']] = a.text
        print(str(len(links)) + ' articles:')
        print(links)
        for page in links:
            pagee = base + page
            print(pagee + ' is parsing...')
            try:
                adr = open(os.path.join(cat, links[page].strip().replace('\"', "").replace("\'", "").replace("«", "")
                                        .replace("»", "")) + '.url', 'w', encoding='utf-8')
                adr.write(pagee)
                adr.close()
            except:
                pass

            req1 = urllib.request.urlopen(pagee)
            html1 = req1.read()
            soap1 = BeautifulSoup(my_url_open(pagee), 'html.parser')

            for soupContent in soap1.find_all('p'):
                try:
                    f = open(os.path.join(cat, links[page].strip().replace('\"', "").replace("\'", "").replace("«", "")
                                          .replace("»", "")) + ".txt", 'a+', encoding='utf-8')
                    f.write(format_sentence(soupContent.text))
                    f.close()
                except:
                    pass

        current_page += 1
        if current_page <= int(page_count):
            try:
                req = urllib.request.urlopen(BASE_SITE + str(current_page))
                html = req.read()
                soap = BeautifulSoup(html, 'html.parser')
            except urllib.error.URLError as e:
                print(e)
                art_count += 1  # 1111
                print('Total errors', art_count)

    print('\nOperation successful.')

def single_page_parse(url, file):
    BASE_SITE = url
    req = urllib.request.urlopen(BASE_SITE)
    html = req.read()

    soap = BeautifulSoup(html, 'html.parser')
    links = []
    articles = soap.find_all('h1', class_='card-title h5')
    for a in articles:
        links.append(BeautifulSoup.find(a, 'a')['href'])

    print(str(len(links)) + ' articles:')
    print(links)
    for page in links:
        pagee = base + page
        print(pagee + ' is parsing...')
        req1 = urllib.request.urlopen(pagee)
        html1 = req1.read()
        soap1 = BeautifulSoup(my_url_open(pagee), 'html.parser')

        for soupContent in soap1.find_all('p'):
            f = open(file, 'a+', encoding='utf-8')
            f.write(format_sentence(soupContent.text))
            f.close()

    print('\nOperation successful.')
