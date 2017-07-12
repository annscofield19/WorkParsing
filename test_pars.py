import requests, json
from bs4 import BeautifulSoup

baseurl = 'https://realt.by/sale/shops/?page=8' # Базовый URL  - https://realt.by/sale/shops/

with open('D:/PYTHON/NCA 03072017/WorkNew/WorkParsing/Offices_Realt_Excel', 'r', encoding='utf-8') as jf: #открываем файл на чтение
    Realt_Excel_dict = json.load(jf) # загружаем из файла данные в словарь Realt_Excel_dict = {'Вид объекта': 'Наименование', 'Вид объекта2': 'Назначение', 'Условия сделки': 'Тип предложения', ...
excel_fields_list = list(Realt_Excel_dict.values()) # Cоздаем лист с полями Ексель - ['Наименование', 'Назначение', 'Тип предложения', 'Контактные данные'...
realt_fields_list = list(Realt_Excel_dict.keys())

with open('D:/PYTHON/NCA 03072017/WorkNew/WorkParsing/Offices_Realt_Fields_Options', 'r', encoding='utf-8') as jf: #открываем файл на чтение
    Excel_options_dict = json.load(jf)

def get_html(url):
    try:
        res = requests.get(url, headers = headers)
    except requests.ConnectionError:
        return

    if res.status_code < 400:
        return res.content
headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
      }

html = get_html(baseurl)
soup = BeautifulSoup(html, "html.parser")

# look for hrefs in titles
table = soup.find_all('div', {'class': 'bd-item'}) # Получаем список с объявлениями на странице

projects = [] # Список со словарями со страницы, где каждый словарь соответствует одному объявлению на странице. Словарь в таком виде, в котором будет записываться в Ексель
# проходимся по каждому объявлению
# for row in table:
#
#     # get hrefs of every page
#     href_name = row.find('a')
#     obj_url = href_name.get("href")
#     html_obj = get_html(obj_url)
#
#     soup1 = BeautifulSoup(html_obj, "html.parser")
#     table = soup1.find_all('tr', {'class': 'table-row'})# Получаем список со всеми необходимыми данными объявления
#
#     project = {}
#     for i in table:  # Проходимся по каждой строке на странице объявления
#         for option in realt_fields_list:  # Прохдимся по каждому параметру из списка всевозможных параметров на странице. Спиосок создан из словаря соответстий поля на реалте и поля в ексель (Oficces_Realt_Excel).
#             if option in i.text:  # Если параметр есть в тексте, то начинаем его обрабатывать
#
#                 realt_answer = i.text.split(option)[1].strip()  # Получаем только ответ
#                 Excel_field = Realt_Excel_dict[option]  # Получаем название поля в Excel
#                 if option == "Ориентировочная стоимость эквивалентна":
#                     print(realt_answer)

# realt_answer = 'Строительство нового торгового центра в Заводском районе. Приглашаем партнеров (торговый центр, магазин, торговое помещение, павильон, киоск, кафе, сфера услуг, салон красоты, парикмахерская, медицина, аптека, здание, банк, торговое место)'
# # osnov_vid = realt_answer.split(")")[-2]
# # print(osnov_vid)
# # # osnov_vid = realt_answer.split(")")[-2].split("(")[1].split(",")[0].lower()
# osnov_vid = realt_answer.split(")")[-2].split("(")[1].lower()
# if ',' in osnov_vid:  # если в скобочках записано более чем один доп вид - т.е. есть запятая. ПОЧТИ ВСЕГДА
#     osnov_vid = realt_answer.split(",")[0]  # если в скобочках записано более чем один доп вид. ПОЧТИ ВСЕГДА
#     # write_into_project_all_vidy(osnov_vid, project, Excel_field, Excel_field2, Excel_field3)
# print(osnov_vid)

def del_coma(string):
    if ',' in string:
        new_string = string.replace(',', '.')
        string = float(new_string)
        return string
    else:
        string = int(string)
        return string

a = '22,5'
if ',' in a:
    print("bbbbbbbbbbbb")
# print(del_coma(a))