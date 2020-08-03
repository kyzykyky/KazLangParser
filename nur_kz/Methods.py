from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import os
import time


def format_sentence(sentence):
    sentence = sentence.split(". ")
    lines = ''
    for s in sentence:
        lines += s + "\n"
    return lines


def replacer(name):
    name = name.replace('?', '').replace('.', '')
    name = name.replace(':', '').replace(';', '').replace('\\', ' ').replace('/', ' ').replace('*', ' ')
    name = name.replace('\'', '').replace('\"', '').replace('»', '').replace('«', '').replace('\n', ' ')
    while name.find('  ') > 0:
        name = name.replace('  ', ' ')
    return name.strip()


def page_action(url, from_=1, till_=20):
    req = urllib.request.urlopen(url)
    html = req.read()
    soap = BeautifulSoup(html, 'html.parser')

    title = soap.find('h1', class_='block-category-header__title').text.strip()
    print(title)
    if not os.path.exists(title):
        os.mkdir(title)

    while from_ != till_:
        print('PARSING PAGE', from_)

        materials = soap.find('div', {"class": "layout-taxonomy-page__content"})
        mats = materials.findAll('article', {"class": "block-infinite__item"})
        links = {}

        for article in mats:
            name = replacer(article.text.strip()[:-10])  # Убрал дату вконце
            link = article.find('a')['href']
            links[name] = link

        for article in links:
            article_action(links[article], article, title)

        from_ += 1
        req = urllib.request.urlopen(url + f'?page={str(from_)}')   # https://kaz.nur.kz/society/?page=N
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
            block = article2.find('article', {"class": 'formatted-body io-article-body js-article-body'})
            text = block.findAll('p')
            for line in text:
                line = BeautifulSoup.get_text(line)
                f = open(os.path.join(dest, article)
                         + ".txt", 'a+', encoding='utf-8')
                f.write(format_sentence(line))
                f.close()
        except urllib.error.HTTPError:
            pass
    else:
        print('Already parsed')
        time.sleep(15)
