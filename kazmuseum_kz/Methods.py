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
    pages = soap.find('div', class_='k2Pagination')
    page_c = int(BeautifulSoup.findAll(pages, 'li')[-1].get_text(strip=True))
    print(Cat + ' has ' + str(page_c) + ' pages.')
    article_c = 0
    for page in range(1, page_c+1):
        lnk = Link + '?start=' + str(article_c)
        req = urllib.request.urlopen(lnk)
        html = req.read()
        soap = BeautifulSoup(html, 'html.parser')

        print('\nParsing page ' + str(page) + ' ' + lnk)
        materials = soap.findAll('a', class_='moduleItemTitle')
        links = {}
        for article in materials:
            link = article.get('href')
            name = replacer(article.get_text(strip=True))
            links[name] = link
        print(links)
        for article in links:
            Article_action(Cat, article, links[article])
        article_c += 10


def Article_action(Cat, name, link):
    link = 'http://www.kazmuseum.kz' + link
    print('Parsing ' + link + ' ...')
    fixed_name = name.replace('\"', "").replace("\'", "").replace("«", "").replace("»", "")
    adr = open(os.path.join(Cat, fixed_name) + '.url', 'w', encoding='utf-8')
    adr.write(link)
    adr.close()
    try:
        req2 = urllib.request.urlopen(link)
        html2 = req2.read()
        soap2 = BeautifulSoup(html2, 'html.parser')
        Block = soap2.find('div', class_='itemView')
        Text = Block.findAll('p')
        for line in Text:
            line = BeautifulSoup.get_text(line)
            f = open(os.path.join(Cat, fixed_name) + ".txt", 'a+', encoding='utf-8')
            line = format_sentence(line)
            f.write(line)
            f.close()
    except UnicodeEncodeError:
        print('Article ' + name + ' ' + link + ' was not parsed due to unicode encode error!')
    except urllib.error.HTTPError:
        pass

