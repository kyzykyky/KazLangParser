from Methods import *


base = 'http://referatikz.ru'
base_site = 'http://referatikz.ru/load/aza_sha_referattar/2/'
req = urllib.request.urlopen(base_site)
html = req.read()

soap = BeautifulSoup(html, 'html.parser')

categories = soap.find('table', class_='catsTable')
categories = BeautifulSoup.find_all(categories, 'tr')
links = {}  # Словарь
print('This page has: '+str(len(categories)) + ' categories:')

for cat in categories:
    name = BeautifulSoup.find(cat, 'a', class_='catName').contents[0].strip()
    link = base + BeautifulSoup.find(cat, 'a', class_='catName')['href']
    links[name] = link
    materials_count = BeautifulSoup.find(cat, 'span', class_='catNumData').get_text(strip=True)
    print(name+'    ' + link + '    Cтатей: ' + materials_count)
del links['Слайдтар']  # Костыль

for cat in links:
    req1 = urllib.request.urlopen(links[cat])
    html1 = req1.read()
    soap1 = BeautifulSoup(html1, 'html.parser')

    page_count = soap1.find('span', class_='pagesBlockuz1').find_all('a', class_='swchItem')[-2].text
    print(cat + ' - страниц ' + page_count)

    for page in range(1, int(page_count)+1):
        print('Page №', page)
        page_ = 1
        articles = BeautifulSoup.find_all(soap1, 'div', class_='eTitle')
        print(articles)
        for article in articles:
            address = base + BeautifulSoup.find(article, 'a')['href']
            print('Parsing ' + address + ' ...')
            req2 = urllib.request.urlopen(address)
            html2 = req2.read()
            soap2 = BeautifulSoup(html2, 'html.parser')

            text = soap2.find('td', class_='eText')  # Плохая разметка на сайте
            lines = ''
            for p in BeautifulSoup.find_all(text, 'p'):
                lines += p.getText()

            print(text)
            # text = format_sentence(text)
            # f = open(cat + '.txt', 'a+', encoding='utf-8')
            # f.write(text)
            # f.close()
        page_ += 1
        req1 = urllib.request.urlopen(links[cat]+'-'+str(page_))
        html1 = req1.read()
        soap1 = BeautifulSoup(html1, 'html.parser')