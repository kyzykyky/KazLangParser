from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import urllib.error
import os


def format_sentence(sentence):
    sentence = sentence.split(". ")
    lines = ''
    for s in sentence:
        if len(s) > 32:
            lines += s + ".\n"
    return lines.strip()


def replacer(name):
    name = name.replace('?', '')
    name = name.replace('.', '').replace('/', '')
    name = name.replace(';', '').replace('|', '')
    name = name.replace(':', '').replace('\\', '')
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
    pages = soap.find('span', class_='navigation')
    page_count = int(BeautifulSoup.findAll(pages, 'a')[-1].get_text(strip=True))
    print('\n' + Cat + ' has ' + str(page_count) + ' pages.')
    for page in range(52, page_count+1):
        l = Link + 'page/' + str(page)
        req1 = urllib.request.urlopen(l)
        html1 = req1.read()
        soap1 = BeautifulSoup(html1, 'html.parser')

        print('\nParsing page ' + str(page) + ' ' + l)
        materials = soap1.find('div', class_='grid')
        materials = materials.findAll(True, {'class': ['short short-thumb',
                                                  'short-tile-inner img-box img-fit',
                                                  'short-tile-text-only-inner fx-col',
                                                  'short short-thumb-left fx-row']})
        links = {}
        for article in materials:
            link = article.get('href')
            name = replacer(article.get_text(strip=True))
            links[name] = link
        print(links)
        for article in links:
            Article_action(Cat, article, links[article])


def Article_action(Cat, article, link):
    print('Parsing ' + link + ' ...')
    adr = open(os.path.join(Cat, article) + '.url', 'w', encoding='utf-8')
    adr.write(link)
    adr.close()
    try:
        req2 = urllib.request.urlopen(link)
        html2 = req2.read()
        soap2 = BeautifulSoup(html2, 'html.parser')
        Block = soap2.find('div', class_='ftext full-text clearfix video-box')
        Text = BeautifulSoup.findAll(Block, 'div', class_='quote')
        for line in Text:
            line = BeautifulSoup.get_text(line)
            f = open(os.path.join(Cat, article) + ".txt", 'a+', encoding='utf-8')
            line = format_sentence(line)
            f.write(line)
            f.close()
    except urllib.error.HTTPError:
        pass
    # except FileNotFoundError:
    #     pass