# Парсер новостей с сайта gismeteo
#https://www.gismeteo.ru/news/

import os.path as path
import datetime
import requests
import json
from bs4 import BeautifulSoup as bs

class News:
    BASE_URL = 'https://www.gismeteo.ru'
    FILE_PATH = 'gismeteo_news.json'
    
    def __init__(self) -> None:
        self.news_list= list()

    def read_news(self):
        url = self.BASE_URL + '/news/'
        result = list()
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
            item_url = self.BASE_URL + sticky_item_a['href']
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
        return result

    def get_news_list(self)->list:
        #Проверяем наличие ранее сохраненного файла json
        if path.exists(self.FILE_PATH) and path.isfile(self.FILE_PATH):
            timestamp = path.getmtime(self.FILE_PATH)
            datestamp = datetime.datetime.fromtimestamp(timestamp)
            fy, fm, fd, fh, _, _, _, _, _ = datestamp.timetuple()
            datestamp = datetime.datetime.now()
            ny, nm, nd, nh, _, _, _, _, _ = datestamp.timetuple()
            #Если дата/время модификации файла json соответствует текущему времени
            #с точностью до часа
            if fy==ny and fm==nm and fd==nd and fh==nh:
                if self.news_list: #и если список уже заполнен,
                    return self.news_list #возвращаем его без чтения
                else: #а если список пустой, читаем информацию из файла json
                    with open(self.FILE_PATH, 'r', encoding='utf-8') as file:
                        return json.load(file)
        #Если дата файла json отличается от сегодняшней или файл json отсутствует
        #Читаем данные с сайта и записываем файл (кэшируем), чтобы не читать одно и тоже
        result = self.read_news()
        # Готовим json для сохранения в файл словаря новостей
        text = json.dumps(result, sort_keys=False, indent=4, ensure_ascii=False)
        #Сохраняем новости в файл json
        with open(self.FILE_PATH, 'w', encoding='utf-8') as file:
            file.write(text)
        return result

    def get_news(self, news_index: int):
        self.news_list = self.get_news_list()
        return self.news_list[news_index]