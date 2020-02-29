from Methods import *


base = 'https://kitaphana.kz'
req = urllib.request.urlopen('https://kitaphana.kz/refkaz.html')
html = req.read()

soap = BeautifulSoup(html, 'html.parser')

materials = soap.find('div', class_='inside')
categories = BeautifulSoup.find_all(materials, 'li')
links = {}  # Словарь
print('This page has: '+str(len(categories)) + ' categories.')
categories.reverse()
categories.pop()
print(categories)
for cat in categories:
    # print(cat)
    # print(BeautifulSoup.find(cat, 'a', class_='category'))
    name = BeautifulSoup.find(cat, 'a', class_='category').contents[0].strip()
    link = base + BeautifulSoup.find(cat, 'a', class_='category')['href']
    links[name] = link
    print(name + '    ' + link)

for cat in links:
    print('\n\nNow parsing', cat, links[cat])
    req1 = urllib.request.urlopen(links[cat])
    html1 = req1.read()
    soap1 = BeautifulSoup(html1, 'html.parser')

    if not os.path.exists(cat):
        os.mkdir(cat)

    table = BeautifulSoup.find(soap1, 'table', class_='table table-hover')

    multi_page = False
    page_count = soap1.find('p', class_='counter').text.strip()
    if page_count is not '':
        page_count = page_count[-1:]
        print('Category has ' + page_count + ' pages')
        multi_page = True
    else:
        print('Category has 1 page')

    if not multi_page:
        for article in BeautifulSoup.find_all(table, 'tr', class_='sectiontableentry1'):  # четные строки
            article_action(article, cat, article.text)
        for article in BeautifulSoup.find_all(table, 'tr', class_='sectiontableentry2'):  # нечетные строки
            article_action(article, cat, article.text)

    elif multi_page:
        article_counter = 0  # Указатель номера строки
        for pages in range(1, int(page_count)+1):
            print('\nParsing page №' + str(pages))
            req1 = urllib.request.urlopen(links[cat] + '?start=' + str(article_counter))
            html1 = req1.read()
            soap1 = BeautifulSoup(html1, 'html.parser')
            table = BeautifulSoup.find(soap1, 'table', class_='table table-hover')
            for article in BeautifulSoup.find_all(table, 'tr', class_='sectiontableentry1'):  # четные строки
                article_action(article, cat, article.text)
            for article in BeautifulSoup.find_all(table, 'tr', class_='sectiontableentry2'):  # нечетные строки
                article_action(article, cat, article.text)
            article_counter += 20

print('Operation successful')


# Пример содержания слолваря links = {'Мәдениеттану': 'https://kitaphana.kz/ru/refkaz/235-madeniettanu.html', 'Педагогика': 'https://kitaphana.kz/ru/refkaz/236-pedagogika.html', 'Психология': 'https://kitaphana.kz/ru/refkaz/237-psikhologia.html', 'Саясаттану': 'https://kitaphana.kz/ru/refkaz/238-sayasattanu.html', 'Тарих': 'https://kitaphana.kz/ru/refkaz/239-tarikh.html', 'Физика': 'https://kitaphana.kz/ru/refkaz/240-fizika.html', 'Химия': 'https://kitaphana.kz/ru/refkaz/242-khimia.html', 'Экономика': 'https://kitaphana.kz/ru/refkaz/243-ekonomika.html', 'Экология': 'https://kitaphana.kz/ru/refkaz/244-ekologia.html'}