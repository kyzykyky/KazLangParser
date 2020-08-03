from http import client
from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import os
import time
from datetime import datetime, timedelta


def format_sentence(sentence):
    sentence = sentence.split(". ")
    lines = ''
    for s in sentence:
        lines += s + "\n"
    return lines


def replacer(name):
    name = name.replace('?', '').replace('.', '').replace('“', '').replace('”', '')
    name = name.replace(':', '').replace(';', '').replace('\\', ' ').replace('/', ' ').replace('*', ' ')
    name = name.replace('\'', '').replace('\"', '').replace('»', '').replace('«', '').replace('\n', ' ')
    while name.find('  ') > 0:
        name = name.replace('  ', ' ')
    return name.strip()


def page_action(url, from_=1, till_=100):  # Работает только до 100
    base = 'https://www.azattyq.org'

    req = urllib.request.urlopen(url + str(from_))
    html = req.read()
    soap = BeautifulSoup(html, 'html.parser')

    title = soap.find('h1', class_='pg-title').text.strip()
    print(title)
    if not os.path.exists(title):
        os.mkdir(title)

    while from_ != till_:
        print('PARSING PAGE', from_, url + str(from_))

        materials = soap.find('div', {"class": "row"})
        mats = materials.findAll('a',
                                 {"class": ["img-wrap img-wrap--t-spac img-wrap--size-3 img-wrap--float img-wrap--xs",
                                            "img-wrap img-wrap--t-spac img-wrap--size-2 img-wrap--float"]})
        links = {}
        for article in mats:
            name = replacer(article['title'].strip())
            link = base + article['href']
            links[name] = link

        for article in links:
            article_action(links[article], article, title)

        from_ += 1
        req = urllib.request.urlopen(url + str(from_))  # https://www.azattyq.org/z/330?p=N
        html = req.read()
        soap = BeautifulSoup(html, 'html.parser')


def article_action(url, article, dest):
    print('Parsing ' + url + ' ...')
    if not os.path.exists(dest + '\\' + article + '.url'):
        adr = open(os.path.join(dest, article)
                   + '.url', 'w', encoding='utf-8')
        adr.write(url)
        adr.close()

        try:
            req2 = urllib.request.urlopen(url)
            html2 = req2.read()
            article2 = BeautifulSoup(html2, 'html.parser')
            block = article2.find('div', {"class": 'wsw'})
            text = str(block.text)  # findAll('p')
            # for line in text:                             #   Начиная с 23.06.2014 Формат теста на странице изменен
            #     line = BeautifulSoup.get_text(line)       #   Пропали <p> почти в каждой новости
            f = open(os.path.join(dest, article)
                     + ".txt", 'a+', encoding='utf-8')
            f.write(format_sentence(text))
            f.close()
        except urllib.error.HTTPError:
            pass
        except client.RemoteDisconnected:
            time.sleep(10)
            article_action(url, article, dest)
        except urllib.error.URLError:
            time.sleep(10)
            article_action(url, article, dest)
    else:
        print('Already parsed')


def date_page_action(url, from_=1, till_=100, year=2020, month=7, day=28):
    base = 'https://www.azattyq.org'  # 2020/7/28?p=N
    _date_ = datetime.strptime(str(year) + '/' + str(month) + '/' + str(day), "%Y/%m/%d")
    date_ = _date_.strftime("%Y/%m/%d")

    url_ = url + date_ + '?p=' + str(from_)
    req = urllib.request.urlopen(url_)
    html = req.read()
    soap = BeautifulSoup(html, 'html.parser')

    title = soap.find('h1', class_='pg-title').text.strip()
    print(title)
    if not os.path.exists(title):
        os.mkdir(title)

    while from_ != till_:
        print('PARSING: ', _date_, url_)

        materials = soap.find('div', {"class": "row"})
        mats = materials.findAll('a',
                                 {"class": ["img-wrap img-wrap--t-spac img-wrap--size-3 img-wrap--float img-wrap--xs",
                                            "img-wrap img-wrap--t-spac img-wrap--size-2 img-wrap--float"]})
        links = {}
        for article in mats:
            name = replacer(article['title'].strip())
            link = base + article['href']
            links[name] = link

        for article in links:
            article_action(links[article], article, title)

        _date_ = _date_ - timedelta(days=1)
        date_ = _date_.strftime("%Y/%m/%d")

        # https://www.azattyq.org/z/330/yyyy/mm/dd?p=N
        url_ = url + date_ + '?p=' + str(from_)
        try:
            req = urllib.request.urlopen(url_)
        except urllib.error.HTTPError:
            time.sleep(15)
            req = urllib.request.urlopen(url_)
        html = req.read()
        soap = BeautifulSoup(html, 'html.parser')
        from_ += 1
        if from_ == 4:
            from_ = 1
