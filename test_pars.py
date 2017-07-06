from bs4 import BeautifulSoup
import requests
import pyexcel as pe
import xlwt
import openpyxl
import os
import json
# with open('D:/PYTHON/2017/Parsing/WorkParsing/Offices_Realt_Excel.json', 'r', encoding='utf-8') as jf: #открываем файл на чтение
#     Realt_Excel_dict = json.load(jf) #загружаем из файла данные в словарь Realt_Excel_dict = {'Вид объекта': 'Наименование', 'Вид объекта2': 'Назначение', 'Условия сделки': 'Тип предложения', ...
# print(Realt_Excel_dict.values())
# excel_fields_list = list(Realt_Excel_dict.values())
# for option in excel_fields_list:
#     print(next((key for key, value in Realt_Excel_dict.items() if value == option), None))


baseurl = 'https://realt.by/sale/shops/?page=1' # Базовый URL  - https://realt.by/sale/shops/

# with open('D:/PYTHON/2017/Parsing/WorkParsing/Offices_Realt_Excel.json', 'r', encoding='utf-8') as jf: #открываем файл на чтение
#     Realt_Excel_dict = json.load(jf) # загружаем из файла данные в словарь Realt_Excel_dict = {'Вид объекта': 'Наименование', 'Вид объекта2': 'Назначение', 'Условия сделки': 'Тип предложения', ...
# excel_fields_list = list(Realt_Excel_dict.values()) # Cоздаем лист с полями Ексель - ['Наименование', 'Назначение', 'Тип предложения', 'Контактные данные'...
# realt_fields_list = list(Realt_Excel_dict.keys())
#
# with open('D:/PYTHON/2017/Parsing/WorkParsing/Offices_Realt_Fields_Options.json', 'r', encoding='utf-8') as jf: #открываем файл на чтение
#     Excel_options_dict = json.load(jf)

def get_html(url):
    try:
        res = requests.get(url)
    except requests.ConnectionError:
        return

    if res.status_code < 400:
        return res.content

def parse(html):

    soup = BeautifulSoup(html, "html.parser")
    # look for hrefs in titles
    table = soup.find_all('div', {'class': 'bd-item'})
    projects = []
    # проходимся по каждому объявлению
    for row in table:
        i=1 # for name of photo
        # get hrefs of all pages
        href_name = row.find('a')
        obj_url = href_name.get("href")
        html_obj = get_html(obj_url)

        soup1 = BeautifulSoup(html_obj, "html.parser")
        table = soup1.find_all('tr', {'class': 'table-row'})
        project = {}
        id_object_name = int(obj_url.split('object/')[1][:-1])
        project['№ Объявления'] = id_object_name
        print(project['№ Объявления'])

        for i in table:
            for option in realt_fields_list:
                if option in i.text:
                    realt_answer = i.text.split(option)[1].strip()
                    if option == "Ориентировочная стоимость эквивалентна":
                        print(i)
string = "Строительство нового торгового центра в Заводском районе. Приглашаем партнеров (торговый центр, магазин, торговое помещение, павильон, киоск, кафе, сфера услуг, салон красоты, парикмахерская, медицина, аптека, здание, банк, торговое место)"
a = string.split(")")[-1]
print(a)
# html = get_html(baseurl)
# parse(html)