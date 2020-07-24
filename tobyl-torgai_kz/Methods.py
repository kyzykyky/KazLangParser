import os
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import urllib.error


def format_sentence(sentence):
    sentence = sentence.split(". ")
    lines = ''
    for s in sentence:
        if len(s) > 32:
            lines += s + ".\n"
    return lines.strip()


def replacer(name):
    name = name.replace('?', '')
    name = name.replace('.', '')
    name = name.replace(';', '')
    name = name.replace(':', '')
    name = name.replace('\'', '').replace('\"', '').replace('»', '').replace('«', '')
    while name.find('  ') > 0:
        name = name.replace('  ', ' ')
    return name


def Cat_action(Cat, Link):
    req = urllib.request.urlopen(Link)
    html = req.read()
    soap = BeautifulSoup(html, 'html.parser')

    if not os.path.exists(Cat):
        os.mkdir(Cat)
    pages = int(soap.find('span', class_='pages').get_text(strip=True)[-1])
    print('\n' + Cat + ' has ' + str(pages) + ' pages.')
    for page in range(1, pages+1):
        l = Link + '/page/' + str(page)
        req1 = urllib.request.urlopen(l)
        html1 = req1.read()
        soap1 = BeautifulSoup(html1, 'html.parser')

        print('\nParsing page ' + str(page) + ' ' + l)
        materials = soap1.find('div', class_='post-listing archive-box')
        materials = BeautifulSoup.findAll(materials, 'a')
        links = {}
        for article in materials:
            link = article.get('href')
            name = replacer(article.get_text(strip=True))
            if name != 'Толығырақ ' and not name.isdigit() and name.find('видео') < 0 and name != '':
                links[name] = link
        print(links)
        for article in links:
            Article_action(Cat, article, links[article])


def Article_action(Cat, article, link):
    print('Parsing ' + link + ' ...')
    adr = open(os.path.join(Cat, article.replace('\"', "").replace("\'", "").replace("«", "").replace("»", ""))
               + '.url', 'w', encoding='utf-8')
    adr.write(link)
    adr.close()
    try:
        req2 = urllib.request.urlopen(link)
        html2 = req2.read()
        soap2 = BeautifulSoup(html2, 'html.parser')
        Block = soap2.find('div', class_='entry')
        Text = Block.findAll('p')
        for line in Text:
            line = BeautifulSoup.get_text(line)
            f = open(os.path.join(Cat, article.replace('\"', "").replace("\'", "").replace("«", "").replace("»", ""))
                     + ".txt", 'a+', encoding='utf-8')
            line = format_sentence(line)
            f.write(line)
            f.close()
    except urllib.error.HTTPError:
        pass


