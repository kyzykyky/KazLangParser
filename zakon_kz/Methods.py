from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import os
import re


def format_sentence(sentence):
    sentence = sentence.split(". ")
    lines = ''
    for s in sentence:
        if s.startswith('Telegram арнасындағы'):
            break
        lines += s + "\n"
    return lines


def replacer(name):
    name = name.replace('?', '').replace('.', '')
    name = name.replace(':', '').replace(';', '').replace('\\', ' ').replace('/', ' ').replace('*', ' ')
    name = name.replace('\'', '').replace('\"', '').replace('»', '').replace('«', '').replace('\n', ' ')
    while name.find('  ') > 0:
        name = name.replace('  ', ' ')
    return name


def fpage_action(url, page=1):
    base = 'https://kaz.zakon.kz'

    req = urllib.request.urlopen(url + str(page))
    html = req.read()
    soap = BeautifulSoup(html, 'html.parser')
    page += 1

    title = soap.find('h1', class_='roboto').text.strip()
    print(title)
    if not os.path.exists(title):
        os.mkdir(title)

    inner_action(base, title, soap)
    print('NOW PARSING', url + str(page))
    pages_action(url, page, base, title)


def pages_action(url, page, base, title):
    req = urllib.request.urlopen(url + str(page))
    html = req.read()
    soap = BeautifulSoup(html, 'html.parser')
    print('NOW PARSING', url + str(page))
    page += 1

    inner_action(base, title, soap)

    pages_action(url, page, base, title)


def inner_action(base, title, soap):
    materials = soap.find('div', {"id": "dle-content"})
    mats = materials.findAll('div', class_="cat_news_item")
    links = {}
    dest = title
    for line in mats:
        lin = line.text.strip()

        # if re.match(r'(\d+-\d+-\d+)', lin):
        #     dest = title + '\\' + lin
        #     if not os.path.exists(dest):      # Вариант с созданием папок с датой публикации
        #         os.mkdir(dest)
        # else:

        try:
            link = base + line.find('a')['href']    # Тут возникает ошибка, если в первый день нет новостей
            name = replacer(lin)[5:]  # Убрал время спереди
            links[name] = link
        except TypeError:
            pass

    for article in links:
        article_action(links[article], article, dest)


def article_action(url, name, dest):

    print('Parsing ' + url + ' ...')
    name = replacer(name)
    if not os.path.exists(dest + '\\' + name):
        adr = open(os.path.join(dest, name)
                   + '.url', 'w', encoding='utf-8')
        adr.write(url)
        adr.close()

        try:
            req2 = urllib.request.urlopen(url)
            html2 = req2.read()
            article2 = BeautifulSoup(html2, 'html.parser')
            block = article2.find('div', class_='fullnews white_block')
            text = block.findAll('p')
            for line in text:
                line = BeautifulSoup.get_text(line)
                f = open(os.path.join(dest, replacer(name))
                         + ".txt", 'a+', encoding='utf-8')
                f.write(format_sentence(line))
                f.close()
        except urllib.error.HTTPError:
            pass
    else:
        print('Already parsed')
