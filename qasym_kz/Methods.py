import os
import re
from bs4 import BeautifulSoup
import urllib.request


def format_sentence(sentence):
    sentence = sentence.split(". ")
    lines = ''
    for s in sentence:
        lines += s + "\n"
    return lines.strip()


def replacer(name):
    name = name.replace('?', '')
    name = name.replace('.', '')
    name = name.replace(';', '')
    name = name.replace(':', '')
    return name


def Cat_action(Cat, Link):
    req = urllib.request.urlopen(Link)
    html = req.read()

    soap = BeautifulSoup(html, 'html.parser')

    if not os.path.exists(Cat):
        os.mkdir(Cat)
    pages = int(soap.findAll('a', class_='page-numbers')[-2].get_text(strip=True))
    print(Cat + ' has ' + str(pages) + ' pages.')
    for page in range(1, pages+1):
        print('Parsing page ' + str(page))
        materials = soap.find('div', class_='uk-grid uk-grid-collapse')
        materials = BeautifulSoup.findAll(materials, 'a')
        links = {}
        for article in materials:
            link = article.get('href')
            name = replacer(article.get_text(strip=True))
            links[name] = link
        print(links)
        for article in links:
            Article_action(Cat, article, links[article])
        l = Link + 'page/' + str(page)
        print(l)
        req = urllib.request.urlopen(l)
        html = req.read()
        soap = BeautifulSoup(html, 'html.parser')


def Article_action(Cat, name, link):
    print('Parsing ' + link + ' ...')
    adr = open(os.path.join(Cat, name) + '.url', 'w', encoding='utf-8')
    adr.write('[InternetShortcut]\n')
    adr.write('URL=%s' % link)
    adr.close()

    req2 = urllib.request.urlopen(link)
    html2 = req2.read()
    soap2 = BeautifulSoup(html2, 'html.parser')
    soap2 = soap2.find('div', class_='block block-single')

    for text in soap2.find_all_next('p'):
        f = open(os.path.join(Cat, name) + ".txt", 'a+', encoding='utf-8')
        f.write(format_sentence(text.get_text(strip=True)))
        f.close()




