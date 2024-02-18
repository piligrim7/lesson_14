# Парсер новостей с сайта gismeteo
#https://www.gismeteo.ru/news/

import requests
import json
from bs4 import BeautifulSoup as bs

result = list()

base_url = 'https://www.gismeteo.ru'
url = base_url + '/news/'

#Создаем словарь из заголовков запросов (Request Headers) на вкладке network (Сеть)
#подраздел Заголовки (Headers) при просмотре кода в браузере по выбранному url
#То есть копируем все что идет ниже параметров, обрамленных двоеточием, и
#форматируем в виде сложаря, добавляя кавычки, запятую между элементами
#Если запрос успешный, пробуем удалять и снова запускать. Таким образом в словаре
#оставляем только те элементы словаря, без которых запрос приходит с ошибкой.
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 YaBrowser/23.11.0.0 Safari/537.36',
    }
response = requests.get(url=url, headers=headers)
soup = bs(response.text, 'html.parser')

sticky_items = soup.find('div', class_='sticky-items')
for sticky_item in sticky_items.contents:
    sticky_item_a = sticky_item.find('a', class_='card')
    item_url = base_url + sticky_item_a['href']
    item_response = requests.get(url=item_url, headers=headers)
    item_soup = bs(item_response.text, 'html.parser')
    item_column = item_soup.find('div', class_=['content-column', 'column1'])
    article_title = item_column.find('article', class_='article-title')
    article = item_column.find('div', class_='article-content').div
    article_text = ''
    for article_content in article.contents:
        if article_content.name == 'p':
            article_text += '\n' + article_content.text
    
    result.append({
        'head':article_title.h1.text,
        'date_time':article_title.time.text,
        'body': article_text.strip('\n')
    })
    
#Готовим json для сохранения в файл словаря городов
text = json.dumps(result, sort_keys=False, indent=4, ensure_ascii=False)
#Сохраняем города и их количество в файл json
with open('gismeteo_news.json', 'w', encoding='utf-8') as file:
    file.write(text)