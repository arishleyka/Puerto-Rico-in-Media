import os
from bs4 import BeautifulSoup
import ssl
from urllib.request import Request, urlopen
import time
import pandas as pd
import os
import pandas as pandasForSortingCSV


os.chdir("/Users/arishleyka/Dropbox/QTM 446w/huffpost")

ssl._create_default_https_context = ssl._create_unverified_context


def get_title():
    title = soup.find(class_='headline').text
    return title


def get_date():
    date = soup.find('time').text
    date = date.split(',')[:2]
    date = ''.join(date)
    return date


def get_author():
    author1 = ""
    author2 = ""
    author = ""
    if soup.find_all(class_='entry-wirepartner__byline') is not None:
        for content in soup.find_all(class_='entry-wirepartner__byline'):
            author = content.text
    if soup.find_all(class_='entry__byline__author') is not None:
        for top in soup.find_all(class_='entry__byline__mini-bio'):
            top.decompose()
        for content in soup.find_all('div', class_='entry__byline__author'):
            author = content.text
    elif soup.find_all(class_='author-card__name') is not None:
        for content in soup.find_all(class_='author-card__name'):
            if len(author1) == 0:
                author1 = content.text
            else:
                author2 = content.text
            author = author1 + " " + author2
    return author


def get_text():
    text = ""
    for paragraph in soup.find_all(class_='primary-cli cli cli-text'):
        text += paragraph.text
    return text



article_info = []
links = []
for i in range(0,290,10):
    original_links = []
    url = "https://www.google.com/search?q=allintitle:+%22Puerto+Rico%22+site:huffpost.com&client=safari&rls=en&ei=bwsxY8n7GcPg8QHFxK3gAg&start=" + str(i) + "&sa=N&ved=2ahUKEwiJ7_PlsbH6AhVDcDwKHUViCyw4ChDy0wN6BAgBEDk&biw=720&bih=772&dpr=2"
    request = Request(url=url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(request).read()
    soup = BeautifulSoup(page, features='lxml')
    for a in soup.find_all('div'):  # only looks at search results
        for link in a.find_all('a', href=True):
            original_links.append(link['href'])

    links = [s for s in original_links if '/url?q=' in s]
    links = [s.replace('/url?q=','') for s in links]
    final_links = [s for s in links if 'www.huffpost.com' in s]
    final_links = [*set(final_links)]

    links = []
    for i in range(len(final_links)):
        links.append(final_links[i].split("&sa=U")[0])

    links = [*set(links)]

    print(links)

    for article in links:
        try:
            request = Request(url=article, headers={'User-Agent': 'Mozilla/5.0'})
            page = urlopen(request).read()
            soup = BeautifulSoup(page, features='lxml')
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
        except:
            pass

        time.sleep(80)

df_article_info = pd.DataFrame(article_info)
df_article_info.to_csv('huffpost_articles1.csv') #1 was up to 60

df = pandasForSortingCSV.read_csv("merged_huffpost.csv")
df = df.drop_duplicates(subset=['text'], keep='last')

df['date'] = pd.to_datetime((df['date']))
df = df.sort_values(by='date', ascending=False)

pd.set_option('display.max_columns', 500)


df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)

df['news source'] = 'HuffPost'
df['political affiliation'] = 'Democratic'

print(len(df))

df.to_csv('formatted_huffpost.csv')

df = pandasForSortingCSV.read_csv("merged_huffpost.csv")
df = df.drop_duplicates(subset=['text'], keep='last')

df['date'] = pd.to_datetime((df['date']))
df = df.sort_values(by='date', ascending=False)

pd.set_option('display.max_columns', 500)


df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)

df['news source'] = 'HuffPost'
df['political affiliation'] = 'Democratic'

print(len(df))

df.to_csv('formatted_huffpost.csv')