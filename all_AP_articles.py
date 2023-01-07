import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from bs4 import BeautifulSoup
import time
import random

os.chdir("C:\\Users\\Tai\\Documents\\qtm446")

options = ChromeOptions()
driver = webdriver.Chrome(options=options)


def get_title():
    title = soup.find('h1', class_='Component-heading-0-2-28')
    ftitle = title.get_text()
    return ftitle


def get_year():
    timestamp = soup.find('span', class_='Timestamp Component-root-0-2-33 Component-timestamp-0-2-32')['title']
    year = timestamp[0:4]
    return year


def get_date():
    timestamp = soup.find('span', class_='Timestamp Component-root-0-2-33 Component-timestamp-0-2-32')['title']
    year = timestamp[0:4]
    date_start = timestamp[1:].index(year)
    date = timestamp[date_start - 6:date_start + 5]
    return date


def get_text():
    entirety = soup.find('div', class_='Article')
    entire_text = entirety.get_text(strip=True)
    text = entire_text[entire_text.index("—") + 2:]
    return text


article_links = []
article_info = []
article_info2 = []
for i in range(0, 281, 10):
    # get google url
    url = "https://www.google.com/search?q=allintitle:+%22Puerto+Rico%22+site:apnews.com&lr=&safe=images&hl=en&as_qdr=all&sxsrf=AOaemvKQaWm2i32t4vJajHTPno5VY7RRoQ:1642745458514&ei=ck7qYbfvHv6nqtsPmuamwAQ&start=" + str(i) + "&sa=N&ved=2ahUKEwi38Ircl8L1AhX-k2oFHRqzCUgQ8tMDegQIARA2&biw=1536&bih=754&dpr=1.25"
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, features="lxml")
    if(soup.find('div', class_="Wt5Tfe") != None):
        soup.find('div', class_="Wt5Tfe").decompose()
    div_source = soup.find('div', class_='v7W49e')   # only looks at search results
    for a in div_source.find_all('a', href=True):    # pulls the urls
        article_links.append(a['href'])
    time_to_sleep = random.randint(3, 5)
    time.sleep(time_to_sleep)
print(len(article_links))
for article in article_links:
    try:
        url = article
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, features="lxml")
        if(soup.find('div', class_= "Article") != None):    # if it is an article
            get_title()
            get_year()
            get_date()
            get_text()
            each_article = {
                'title': get_title(),
                'year': get_year(),
                'date': get_date(),
                'text': get_text(),
                'url': url,
            }
            article_info.append(each_article)
        else:
            pass
    except:
        pass
df_article_info = pd.DataFrame(article_info)
df_article_info.to_csv('AP_articles.csv')
