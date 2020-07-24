import os
from bs4 import BeautifulSoup
import urllib.request
import urllib.error


def format_sentence(sentence):
    sentence = sentence.split(". ")
    lines = ''
    for s in sentence:
        if len(s) > 25:
            lines += s + ".\n"
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
        l = Link + 'page/' + str(page)
        req = urllib.request.urlopen(l)
        html = req.read()
        soap = BeautifulSoup(html, 'html.parser')

        print('\nParsing page ' + str(page) + ' ' + l)
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


def Article_action(Cat, name, link):
    try:
        print('Parsing ' + link + ' ...')
        fixed_name = name.replace('\"', "").replace("\'", "").replace("«", "").replace("»", "")
        adr = open(os.path.join(Cat, fixed_name) + '.url', 'w', encoding='utf-8')
        adr.write(link)
        adr.close()

        req2 = urllib.request.urlopen(link)
        html2 = req2.read()
        soap2 = BeautifulSoup(html2, 'html.parser')
        Text = soap2.findAll('p')
        for line in Text:
            line = BeautifulSoup.get_text(line)
            f = open(os.path.join(Cat, fixed_name) + ".txt", 'a+', encoding='utf-8')
            Line = format_sentence(line)
            f.write(Line)
            f.close()
    except urllib.error.HTTPError:
        print('urllib.error.HTTPError: HTTP Error 499: Request has been forbidden by antivirus')



