from Methods import *


base = 'https://bankreferatov.kz'
req = urllib.request.urlopen('https://bankreferatov.kz/kazaksha-referattar')
html = req.read()

soap = BeautifulSoup(html, 'html.parser')

materials = soap.find('table', class_='contentpane')
# print(materials)
categories = BeautifulSoup.find_all(materials, 'li')
links = {}  # Словарь
print('This page has: '+str(len(categories)) + ' categories.')
for cat in categories:
    name = BeautifulSoup.find(cat, 'a', class_='category').text.strip()
    link = base + BeautifulSoup.find(cat, 'a', class_='category')['href']
    links[name] = link
    mats = BeautifulSoup.find(cat, 'span', class_='small').get_text(strip=True)
    print(name+'    ' + link + '   Статей - ' + mats)

for cat in links:
    print('\n\nNow parsing', cat, links[cat])
    req1 = urllib.request.urlopen(links[cat])
    html1 = req1.read()
    soap1 = BeautifulSoup(html1, 'html.parser')

    table = BeautifulSoup.find(soap1, 'table', class_='contentpane')

    multi_page = False
    page_count = soap1.find('ul', class_='pagination')
    if page_count is not None:
        page_count = BeautifulSoup.find_all(page_count, 'li')[-4].text.strip()
        print('Category has ' + page_count + ' pages')
        multi_page = True
    else:
        print('Category has 1 page')

    if not os.path.exists(cat):
        os.mkdir(cat)  # make folder

    if not multi_page:
        for article in BeautifulSoup.find_all(soap1, 'tr', class_='sectiontableentry1'):  # четные строки
            article_action(article, cat, article.text)
        for article in BeautifulSoup.find_all(soap1, 'tr', class_='sectiontableentry2'):  # нечетные строки
            article_action(article, cat, article.text)

    elif multi_page:
        article_counter = 0  # Указатель номера строки
        for pages in range(1, int(page_count) + 1):
            print('\nParsing page №' + str(pages))
            req1 = urllib.request.urlopen(links[cat] + '?start=' + str(article_counter))
            html1 = req1.read()
            soap1 = BeautifulSoup(html1, 'html.parser')
            # table = BeautifulSoup.find(soap1, 'table', class_='contentpane')
            for article in BeautifulSoup.find_all(soap1, 'tr', class_='sectiontableentry1'):  # нечетные строки
                article_action(article, cat, article.text)
            for article in BeautifulSoup.find_all(soap1, 'tr', class_='sectiontableentry2'):  # четные строки
                article_action(article, cat, article.text)
            article_counter += 10

    print('Operation successful')