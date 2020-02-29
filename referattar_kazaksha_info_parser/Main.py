from Methods import *


base_site = 'https://referattar.kazaksha.info'
req = urllib.request.urlopen(base_site)
html = req.read()
soap = BeautifulSoup(html, 'html.parser')

materials = soap.find('div', class_='textwidget')
categories = BeautifulSoup.find_all(materials, 'li')
links = {}
print('This page has: '+str(len(categories)) + ' categories.')
for cat in categories:
    name = BeautifulSoup.find(cat, 'a').contents[0].strip()
    link = BeautifulSoup.find(cat, 'a')['href']
    links[name] = link
    print(name+'    ' + link)

for cat in links:
    print('\n\nNow parsing', cat, links[cat])
    req1 = urllib.request.urlopen(links[cat])
    html1 = req1.read()
    soap1 = BeautifulSoup(html1, 'html.parser')

    if not os.path.exists(cat):
        os.mkdir(cat)

    multi_page = False
    page_count = soap1.find('div', class_='wp-pagenavi')
    if page_count is not None:
        page_count = BeautifulSoup.find_all(page_count, 'a')
        try:
            page_count = page_count[-3].text
        except IndexError:
            page_count = '2'
        print('Category has ' + page_count + ' pages')
        multi_page = True
    else:
        print('Category has 1 page')

    if multi_page:
        for page in range(1, int(page_count)+1):
            print('\nParsing page №' + str(page))
            for article in soap1.find_all('h2', class_='post-title entry-title'):
                article_action(article, cat, article.text)
            req1 = urllib.request.urlopen(links[cat]+'/page/'+str(page))
            html1 = req1.read()
            soap1 = BeautifulSoup(html1, 'html.parser')
    else:
        for article in soap1.find_all('h2', class_='post-title entry-title'):
            article_action(article, cat, article.text)

print('Operation successful')