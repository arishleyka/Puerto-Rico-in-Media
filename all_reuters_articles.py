import os
import pandas as pd
from bs4 import BeautifulSoup  # for html with beautifulsoup
from selenium import webdriver  # for driver use
from selenium.webdriver.chrome.options import Options as ChromeOptions

from selenium.webdriver.chrome.service import Service

# os.chdir("C:\\Users\\Tai\\Documents\\qtm446")
# ser = Service("C:\\Users\\Tai\\Documents\\qtm446\\chromedriver.exe")
# op = webdriver.ChromeOptions()
# s = webdriver.Chrome(service=ser, options=op)
os.chdir("C:\\Users\\Tai\\Documents\\qtm446")

options = ChromeOptions()
s = webdriver.Chrome(options=options)


url = "https://www.google.com/search?hl=en&as_q=%22Puerto+Rico%22&as_epq=&as_oq=&as_eq=&as_nlo=&as_nhi=&lr=lang_en&cr=&as_qdr=all&as_sitesearch=reuters.com&as_occt=title&as_filetype=&tbs="
s.get(url)
html = s.page_source
soup = BeautifulSoup(html, features="lxml")


def get_title():
    if(url[24:31] == "article"):
        title = soup.find('h1', class_="Headline-headline-2FXIq Headline-black-OogpV ArticleHeader-headline-NlAqj").get_text()
        return title
    else:
        for read in soup.find(
                class_="Text__text___3eVx1j Text__dark-grey___AS2I_p Text__medium___1ocDap Text__heading_2___sUlNJP Heading__base___1dDlXY Heading__heading_2___3f_bIW"):
            return read


register_now = "Register now for FREE unlimited access to Reuters.com"


def get_text():
    if(url[24:31] == "article"):
        full_article = soup.find_all('div', class_="ArticleBodyWrapper")
        text = full_article.find_all('p')
        text.get_text()
        return text
    else:
        for read in soup.find_all(class_="ArticleBody__content___2gQno2 paywall-article").text:
            if register_now in read:
                text_corrected = read.replace("Register now for FREE unlimited access to Reuters.com", "")
                text_corrected = text_corrected.replace("(Reuters)", "")
                text_corrected = text_corrected.split("Reporting by", 1)
                text_final = text_corrected[0]
                return text_final
            else:
                return read


date = ""


def get_date():
    if (url[24:31] == "article"):
        date = soup.find('time', class_="TextLabel__text-label___3oCVw TextLabel__gray___1V4fk TextLabel__small-all-caps___2Z2RG ArticleHeader-date-Goy3y").get_text()
        return date
    else:
        for read in soup.find(class_="DateLine__date___12trWy"):
            return read


def get_year():
    if (url[24:31] == "article"):
        year = date[len(date)-4:len(date):1]
        return year
    else:
        for date in soup.find(class_="DateLine__date___12trWy"):
            year_split = date.split(",")
            year = year_split[1]
            return year


article_links = []
article_info = []
# reuters_only = "reuters.com"
for i in range(0, 1, 10):
    url = "https://www.google.com/search?q=allintitle:+%22Puerto+Rico%22+site:reuters.com&lr=lang_en&hl=en&as_qdr=all&tbs=lr:lang_1en&ei=cEjqYZqcI7GDwbkP1v2Z4A8&start=" + str(
        i) + "&sa=N&ved=2ahUKEwialN_-kcL1AhWxQTABHdZ-Bvw4ChDy0wN6BAgBEDw&biw=720&bih=772&dpr=2"
    s.get(url)
    html = s.page_source
    soup = BeautifulSoup(html, features="lxml")
    if (soup.find('div', class_="EyBRub") != None):
        soup.find('div', class_="EyBRub").decompose()
    div_source = soup.find('div', class_='v7W49e')
    for a in div_source.find_all('a', href=True):  # pulls the urls
        article_links.append(a['href'])

print(article_links)
reuters_only_text = "https://www.reuters.com"
for article in article_links:
    if (article[0:len(reuters_only_text)] == reuters_only_text):
        url = article
        s.get(url)
        html = s.page_source
        soup = BeautifulSoup(html, features="lxml")
        if soup.find('div', class_="fusion-app") != None:
            get_year()
            get_date()
            get_text()
            get_year()
            each_article = {
                'title': get_title(),
                'year': get_year(),
                'date': get_date(),
                'text': get_text(),
                'url': url
            }
            article_info.append(each_article)
        else:
            pass
    else:
        pass

df = pd.DataFrame(article_info)
df.to_csv('Reuters_articles.csv')

df = pandasForSortingCSV.read_csv("Fall_Reuters.csv")

df['text'] = df['text'].str.split('-')

df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)


for a in range(0,312):  # erases irrelevant info such as [location] (Reuters)
    try:
        if len(df.iloc[a]['text']) > 1 and len(df.iloc[a]['text'][0]) == 26: #san juan
            del df.iloc[a]['text'][0]
        elif len(df.iloc[a]['text']) > 1 and "(Reuters)" in df.iloc[a]['text'][0]:
            del df.iloc[a]['text'][0]
    except:
        pass

df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)


for a in range(0,313):
    try:
        df.iloc[a]['text'] = ''.join(df.iloc[a]['text'])
    except:
        pass

df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)

print(df['text'])
df.to_csv('Fall_Reuters.csv')

