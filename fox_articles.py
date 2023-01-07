import os
from bs4 import BeautifulSoup
import ssl
from urllib.request import Request, urlopen
import time
import pandas as pd

os.chdir("/Users/arishleyka/Dropbox/QTM 446w/fox")

ssl._create_default_https_context = ssl._create_unverified_context


def delete():
    for top in soup.find_all(class_='caption'):
        top.decompose()

    for strong in soup.find_all('strong'):
        strong.decompose()


def get_title():
    title = soup.find('h1', class_="headline").text
    return title


def get_date():
    date = soup.find('time').text
    date_split = date.split(':')
    date = date_split[0]
    date = date[:len(date) - 2]
    return date


def get_author():
    author = ""
    for name in soup.find_all(class_='author-byline'):
        for z in name.find_all('span'):
            author += z.text
    return author.partition("By")[2].split(',')[0].strip()


def get_text():
    copyright_text = ""
    copyright_text2 = ""
    for copy in soup.find_all(class_='copyright'):
        if len(copyright_text) == 0:
            copyright_text = copy.text
        else:
            copyright_text2 = copy.text

    copyright_text = soup.find(class_='copyright').text
    successfully = soup.find(class_='success hide').text
    dek = soup.find(class_='dek').text

    text = ""
    for content in soup.find_all(class_='article-body'):
        for paragraph in content.find_all('p'):
            text += paragraph.text

    text = text.replace(copyright_text, '')
    text = text.replace(copyright_text2, '')
    text = text.replace(successfully, '')
    text = text.replace(dek, '')

    contribute = "The Associated Press contributed to this report"
    if contribute in text:
        text = text.replace(contribute, '')

    return text


article_info = []
links = []
for i in range(0,200,10):
    original_links = []
    url = "https://www.google.com/search?q=allintitle:+%22Puerto+Rico%22+site:foxnews.com&client=safari&rls=en&ei=3SUiY4_gDqukqtsPrquH0AU&start="+ str(i) + "&sa=N&ved=2ahUKEwjPwozy_JT6AhUrkmoFHa7VAVo4ChDy0wN6BAgBEDk&biw=720&bih=772&dpr=2"
    request = Request(url=url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(request).read()
    soup = BeautifulSoup(page, features='lxml')
    for a in soup.find_all('div'):  # only looks at search results
        for link in a.find_all('a', href=True):
            original_links.append(link['href'])

    links = [s for s in original_links if '/url?q=' in s]
    links = [s.replace('/url?q=','') for s in links]
    final_links = [s for s in links if 'www.foxnews.com' in s]
    final_links = [*set(final_links)]

    links = []
    for i in range(len(final_links)):
        links.append(final_links[i].split("&sa=U")[0])

    print(links)

    for article in links:
        try:
            request = Request(url=article, headers={'User-Agent': 'Mozilla/5.0'})
            page = urlopen(request).read()
            soup = BeautifulSoup(page, features='lxml')
            delete()
            get_title()
            get_author()
            get_date()
            get_text()
            each_article = {
                'title': get_title(),
                'author': get_author(),
                'date': get_date(),
                'text': get_text(),
                'url': article,
            }
            article_info.append(each_article)
            temp = get_title()
            print(temp)
            print(get_author())
            print(article)
        except:
            pass

        time.sleep(80)

df_article_info = pd.DataFrame(article_info)
df_article_info.to_csv('fox_articles.csv') # 1 was up to 60, 60 to 120, 120 to 200 #4 210 to 280

import pandas as pd
import os
import pandas as pandasForSortingCSV

df = pandasForSortingCSV.read_csv("merged_fox.csv")
df = df.drop_duplicates(subset=['text'], keep='last')

df['date'] = pd.to_datetime((df['date']))
df = df.sort_values(by='date', ascending=False)

df['author'] = df['author'].str.split('|')

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)

for a in range(0,132):  # erases irrelevant info such as "| fox news| from the author column"
    try:
        if len(df.iloc[a]['author']) > 1:
            del df.iloc[a]['author'][1:]
    except:
        pass

df['author'] = df['author'].str.join('')


df['text'] = df['text'].str.split('–')

for a in range(0,132):  # erases irrelevant info such as [location] (Reuters)
    try:
        if len(df.iloc[a]['text']) > 1 and len(df.iloc[a]['text'][0]) == 22: #san juan
            del df.iloc[a]['text'][0]
        elif len(df.iloc[a]['text']) > 1 and "(AP)" in df.iloc[a]['text'][0]:
            del df.iloc[a]['text'][0]
    except:
        pass

df['text'] = df['text'].str.join('')
df['news source'] = 'Fox'
df['political affiliation'] = 'Conservative'

df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)

print(len(df))

df.to_csv('formatted_fox.csv')








