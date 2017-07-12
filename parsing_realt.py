from bs4 import BeautifulSoup
import requests
import pyexcel as pe
import xlwt
import openpyxl
import json
from datetime import datetime
import time
import random

baseurl = 'https://realt.by/sale/restorant-cafe/object/1054855/' # Базовый URL  - https://realt.by/sale/shops/

headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
      }
with open('D:/PYTHON/NCA 03072017/WorkNew/WorkParsing/Offices_Realt_Excel', 'r', encoding='utf-8') as jf: #открываем файл на чтение
    Realt_Excel_dict = json.load(jf) # загружаем из файла данные в словарь Realt_Excel_dict = {'Вид объекта': 'Наименование', 'Вид объекта2': 'Назначение', 'Условия сделки': 'Тип предложения', ...
excel_fields_list = list(Realt_Excel_dict.values()) # Cоздаем лист с полями Ексель - ['Наименование', 'Назначение', 'Тип предложения', 'Контактные данные'...
realt_fields_list = list(Realt_Excel_dict.keys())

with open('D:/PYTHON/NCA 03072017/WorkNew/WorkParsing/Offices_Realt_Fields_Options', 'r', encoding='utf-8') as jf: #открываем файл на чтение
    Excel_options_dict = json.load(jf)


def get_html(url): # Получаем html. На вход url страницы
    try:
        res = requests.get(url, headers = headers)
    except requests.ConnectionError:
        return
    if res.status_code < 400:
        return res.content


def get_dol_kurs(url = 'http://www.nbrb.by/API/ExRates/Rates/145'): # Получаем курс доллара На вход - запрос апи с сайта нацбанка
    byte_kurs = get_html(url) # b'{...}
    dict_kurs = json.loads(byte_kurs) # {...}
    kurs = dict_kurs['Cur_OfficialRate']
    return kurs # 1.9750


def get_today_date(): # Получаем егодняшнюю дату в формате '13.07.2017'
    date = datetime.strftime(datetime.now(), "%d.%m.%Y")
    return date


def del_space_and_make_integer(string): # Для удаления спец пробела в ЦЕНЕ - 1 670. Возвращает целое число без пробела. На вход - строка с ценой '1 670' or '879'
    string = str(string)
    if ' ' in string:
        new_string = string.replace(' ', '')
        string = float(new_string)
        return string
    else:
        string = float(string)
        return string

def del_coma(string):
    if ',' in string:
        string = string.replace(',', '.')
        return string
    else:
        return string

def get_coords(soup, project): # Для каждого объявления находит координату с Яндекс карты, На вход - объект суп страницы с объявлением и словарь, куда записываются координаты
    table = soup.find_all('script', {'type': 'text/javascript'}) # Находим все объекты на странице с заданными параметрами
    for i in table:
        string = i.text
        if 'ymaps' in string: # Если в строке есть 'ymaps' - то данный скрипт содержит координаты
            coordinates = string.split('center: [')[1].split(']')[0]
            X = coordinates.split(', ')[0]
            Y = coordinates.split(', ')[1]
            project['XCoord'] = X
            project['YCoord'] = Y


def write_webpage_to_html(html_number, html_obj, folder_path):  # Сохраняет веб-страницу в файл формата .html. На вход - уникальный номер объявления (для формирования имени), html_obj = get_html(obj_url), где obj_url - url странички, которую записывают в html-файл и folder_path - путь к папке, куда сохранять файлы
    name_html = '{}/{}.html'.format(folder_path, html_number)
    with open(name_html, 'wb') as file:
        file.write(html_obj)


def get_photos(soup, project, folder_path): # НЕ ИСПОЛЬЗУЕТСЯ Загружает фотографии со страницы с объявлением. На вход soup - объект суп для странички с объявлением (В данном случае - soup1), project - словарь, где записан уникальный номер объявления (для названия фото) и folder_path - путь к папке, куда сохранять файлы
    i = 1 # Для названия фотографий
    photos = soup.find_all('div', {'class': 'photo-item'})  # получаем список с фотографиями объявления
    if photos:  # если фото на странице есть
        for photo in photos:
            lnk = photo.find('img').get('src') # Получаем ссылку на каждое фото
            nametemp = "{}/{}_{}.jpeg".format(folder_path, project['ID_object'], i)
            i +=1
            with open(nametemp, "wb") as f:
                real_photo = get_html(lnk)
                f.write(real_photo)

def get_table_coords(project, i): # НЕ ИСПОЛЬЗУЕТСЯ Для объявлений, где есть координаты в таблице на странице - для Общественно - деловой зоны их нет. На вход - project - словарь, куда записываются координты,  i - (for i in table, где table - список со всеми полями и ответами со старнички с объявлением) table = soup1.find_all('tr', {'class': 'table-row'})
    if 'Координаты для онлайн карт' in i.text:
        coordinates = i.text.split('Координаты для онлайн карт')[1].strip()
        project['Xcoord'] = coordinates.split(' ')[0]
        project['Ycoord'] = coordinates.split(' ')[1]

def write_projects_into_new_excel(projects, options, excel_path): # НЕ ИСПОЛЬЗУЕТСЯ записывает список словарей в новый файл ексель, projects - список словарей, где ключ - название поля, значение - значение для строки;  options  - список значений полей для ексель; excel_path - полный путь к новому екселю
    wb = xlwt.Workbook()
    ws = wb.add_sheet("Sheet")
    row = 0
    line = 0
    for option in options:
        ws.write(row, line, option)
        line += 1
    for project in projects:
        line = 0
        row += 1
        for option in options:
            if option in project:
                ws.write(row, line, project[option])
                line += 1
    wb.save(excel_path)


def write_into_cell(ws, project, row_num):
    for i in range(1, 70):  # Видимо 70 - количество столбцов в екселе максимальное)))
        # for field in excel_fields_list:
        for field in list(project.keys()):  # проходимся по полям которые есть в конкретном project
            if field == ws.cell(row=3,
                                column=i).value and field == "Ссылка на html":  # и если поле в project совпадает с полем в ексель и это поле для гиперссылки  то записываем в строку
                ws.cell(row=row_num, column=i).hyperlink = project[field]
            elif field == ws.cell(row=3,
                                  column=i).value:  # и если поле в project совпадает с полем в ексель то записываем в строку
                ws.cell(row=row_num, column=i).value = project[field]

def add_projects_into_existing_excel(projects, excel_path = "MyExcel.xlsx"):
    wb = openpyxl.load_workbook(filename=excel_path)
    # Выбираем лист
    ws = wb.get_sheet_by_name('Sheet')
    row_num = ws.max_row # находим последнюю строку (чтобы записывать новые данные в следующую)
    for project in projects:
        row_num +=1
        write_into_cell(ws, project, row_num)
    wb.save(excel_path)

def add_project_into_existing_excel(project, excel_path = "MyExcel.xlsx"):
    wb = openpyxl.load_workbook(filename=excel_path)
    # Выбираем лист
    ws = wb.get_sheet_by_name('Sheet')
    row_num = ws.max_row  # находим последнюю строку (чтобы записывать новые данные в следующую)
    row_num += 1
    write_into_cell(ws, project, row_num)
    wb.save(excel_path)



def get_area(realt_answer): # Получаем из ответа только площадь - избавляемся от м², где realt_answer - ответ на реалте
    return realt_answer.split('м²')[0].strip()

def get_hight(realt_answer): # Получаем из ответа только площадь - избавляемся от м², где realt_answer - ответ на реалте
    return realt_answer.split('м')[0].strip()

# 5 ФУНКЦИЙ ДЛЯ ПОЛУЧЕНИЯ ЦЕНЫ


def get_price(realt_answer, project, Excel_field): # Функция удаляет пробел в цене если он есть и записывает в project цену переведенную в долларах
    realt_answer = del_coma(realt_answer)
    realt_answer = del_space_and_make_integer(realt_answer)
    project[Excel_field] = int(realt_answer / get_dol_kurs())

def get_price_whole_lot(realt_answer, project, Excel_field): # Функция удаляет пробел в цене если он есть и записывает в project цену переведенную в долларах С ПОМЕТКОЙ ЧТО ЦЕНА УКАЗАНА ЗА ВЕСЬ ЗЕМЕЛЬНЫЙ УЧАСТОК
    realt_answer = del_coma(realt_answer)
    realt_answer = del_space_and_make_integer(realt_answer)
    project[Excel_field] = '{} !Цена указана за весь участок'.format(int(realt_answer / get_dol_kurs()))

def check_price(realt_answer, project, Excel_field): # Функция проверяет есть ли в цене строки '—', 'до ' или нет. и записывает корректную (если были строки) в долларах
    if '—' in realt_answer:
        realt_answer = realt_answer.split('—')[0].strip()
        get_price(realt_answer, project, Excel_field)
    elif 'до ' in realt_answer:
        realt_answer = realt_answer.split('до ')[1].strip()
        get_price(realt_answer, project, Excel_field)
    else:
        get_price(realt_answer, project, Excel_field)

def check_price_whole_lot(realt_answer, project, Excel_field): # Функция проверяет есть ли в цене строки '—', 'до ' или нет. и записывает корректную (если были строки) в долларах
    if '—' in realt_answer:
        realt_answer = realt_answer.split('—')[0].strip()
        get_price_whole_lot(realt_answer, project, Excel_field)
    elif 'до ' in realt_answer:
        realt_answer = realt_answer.split('до ')[1].strip()
        get_price_whole_lot(realt_answer, project, Excel_field)
    else:
        get_price_whole_lot(realt_answer, project, Excel_field)

def get_finish_price(realt_answer, project, Excel_field): # где realt_answer - ответ на реалте, project - словарь, куда записывается итоговая цена,   Excel_field = Realt_Excel_dict[option] - Получаем название поля в Excel, option - название поля на реалте
    # print(realt_answer) - сто пятьсот вариантов
    if ", " in realt_answer:
        realt_answer = realt_answer.split(', ')[1].split('руб')[0].strip()  # '355—395' or '356' or '1 876' or '1 355—1 395' or 'до 2 157'
        check_price(realt_answer, project, Excel_field)
    elif 'договор' in realt_answer:
        project[Excel_field] = 'Цена договорная'
    else:
        if 'руб/кв.м' in realt_answer:
            realt_answer = realt_answer.split(' руб/кв.м')[0].strip()
            check_price(realt_answer, project, Excel_field)
        elif 'руб/м²' in realt_answer:
            realt_answer = realt_answer.split(' руб/м²')[0].strip()
            check_price(realt_answer, project, Excel_field)
        else: # значит стоимость дана только за весь земельный участок и в строке есть слово "руб"
            realt_answer = realt_answer.split(' руб')[0].strip()
            check_price_whole_lot(realt_answer, project, Excel_field)

# 2 ФУНКЦИИ ДЛЯ ОПРЕДЕЛЕНИЯ ВИДА, НАЗНАЧЕНИЯ И НАИМЕНОВАНИЯ ОБЪЕКТА
def write_into_project_all_vidy(osnov_vid, project, Excel_field, Excel_field2, Excel_field3):
    project[Excel_field] = Excel_options_dict[Excel_field][osnov_vid]
    project[Excel_field2] = Excel_options_dict[Excel_field2][osnov_vid]
    project[Excel_field3] = Excel_options_dict[Excel_field3][osnov_vid]

def get_finish_vid_object(realt_answer, project, Excel_field, Excel_field2, Excel_field3): # из многообразия того что записано, нужно определить основной вид и в определить по нему Вид объекта, Наименование и Назначение
    if "(" in realt_answer:
        osnov_vid = realt_answer.split(" (")[0].strip().lower()
        if len(osnov_vid) <= 18: # "торговое помещение" - 18 символов. Самое длинное из возможных вариантов на реалте. Но бывает что до скобок записана ерунда и она тоже меньше 18 символов
            try:
                write_into_project_all_vidy(osnov_vid, project, Excel_field, Excel_field2, Excel_field3)
            except KeyError:
                osnov_vid = realt_answer.split(")")[-2].split("(")[1].lower()# [-2] - второй элемент с конца, т.к. первый элемент с конца - пустая строка
                if ',' in osnov_vid: # если в скобочках записано более чем один доп вид - т.е. есть запятая. ПОЧТИ ВСЕГДА
                    osnov_vid = osnov_vid.split(",")[0]
                    write_into_project_all_vidy(osnov_vid, project, Excel_field, Excel_field2, Excel_field3)
                else:
                    write_into_project_all_vidy(osnov_vid, project, Excel_field, Excel_field2, Excel_field3)
        else: # если символов до "(" большее 18, то основной вид записан первым после послдней скобки "("
            osnov_vid = realt_answer.split(")")[-2].split("(")[1].lower()
            if ',' in osnov_vid: # если в скобочках записано более чем один доп вид - т.е. есть запятая. ПОЧТИ ВСЕГДА
                osnov_vid = osnov_vid.split(",")[0]  # если в скобочках записано более чем один доп вид. ПОЧТИ ВСЕГДА
                write_into_project_all_vidy(osnov_vid, project, Excel_field, Excel_field2, Excel_field3)
            else:
                write_into_project_all_vidy(osnov_vid, project, Excel_field, Excel_field2, Excel_field3)
    else:
        osnov_vid = realt_answer.lower()
        write_into_project_all_vidy(osnov_vid, project, Excel_field, Excel_field2, Excel_field3)

def get_contacts(realt_answer, project, Excel_field):
    if 'Пожалуйста, скажите что Вы нашли это объявление на сайте Realt.by' in realt_answer:
        project[Excel_field] = realt_answer.split('Пожалуйста, скажите что Вы нашли это объявление на сайте Realt.by')[1].strip()
    else:
        project[Excel_field] = realt_answer

# 5 функций для определения адреса
def get_street(realt_answer, project, Excel_field, Excel_field2):
    street_elem = realt_answer.split(".")[0]  # Никольская ул
    realt_elem_name = street_elem.split(' ')[-1]  # ул
    realt_street_name = street_elem.split(realt_elem_name)[0].strip()  # 40 лет Победы
    project[Excel_field2] = Excel_options_dict[Excel_field2][realt_street_name]

def get_street_not_in_dict(realt_answer, project, Excel_field, Excel_field2):
    street_elem = realt_answer.split(".")[0]  # Никольская ул
    realt_elem_name = street_elem.split(' ')[-1]  # ул
    realt_street_name = street_elem.split(realt_elem_name)[0].strip()  # 40 лет Победы
    project[Excel_field2] = "{} - не из классификатора".format(realt_street_name)

def get_elem(realt_answer, project, Excel_field, Excel_field2):
    street_elem = realt_answer.split(".")[0]  # Никольская ул
    realt_elem_name = street_elem.split(' ')[-1]  # ул
    project[Excel_field] = Excel_options_dict[Excel_field][realt_elem_name]

def get_elem_not_in_dict(realt_answer, project, Excel_field, Excel_field2):
    street_elem = realt_answer.split(".")[0]  # Никольская ул
    realt_elem_name = street_elem.split(' ')[-1]  # ул
    project[Excel_field] = "{} - не из классификатора".format(realt_elem_name)

def get_full_address(realt_answer, project, Excel_field, Excel_field2, Excel_field3, Excel_field4, id_object_name): # Никольская ул., 66-2, 40 лет Победы ул., 66-2,
    if "." in realt_answer:
        try:
            get_street(realt_answer, project, Excel_field, Excel_field2)
        except IndexError:
            print("Для объекта с номером {} - Невозможно определить улицу".format(id_object_name))
        except KeyError:
            get_street_not_in_dict(realt_answer, project, Excel_field, Excel_field2)
        try:
            get_elem(realt_answer, project, Excel_field, Excel_field2)
        except IndexError:
            print("Для объекта с номером {} - Невозможно определить улицу".format(id_object_name))
        except KeyError:
            get_elem_not_in_dict(realt_answer, project, Excel_field, Excel_field2)

    if "," in realt_answer:
        house_korp = realt_answer.split(',')[1].strip()  # 66-2 или 66
        if "-" in house_korp: # значит есть корпус
            house = house_korp.split('-')[0]
            if " " in house:
                house = house.split(' ')[0]
            project[Excel_field3] = house
            korp = house_korp.split('-')[1]
            if " " in korp:
                korp = korp.split(' ')[0]
            project[Excel_field4] = korp
        else:
            house = house_korp.split('-')[0]
            if " " in house:
                house = house.split(' ')[0]
            project[Excel_field3] = house



def parse_object(obj_url, project={}):
    html_obj = get_html(obj_url)
    soup1 = BeautifulSoup(html_obj, "html.parser")
    table = soup1.find_all('tr', {'class': 'table-row'})  # Получаем список со всеми необходимыми данными объявления

    id_object_name = int(
        obj_url.split('object/')[1][:-1])  # из url страницы объявления оставляем только уникальный номер
    project['№ Объявления'] = id_object_name
    project['Дата актуальности предложения'] = get_today_date()  # Сегодняшняя дата (13.07.2017)
    project['Ссылка на html'] = '{}/{}.html'.format("D:/PYTHON/NCA 03072017/WorkNew/WorkParsing/HTMLs", id_object_name)
    project['Источник'] = "Realt.by"
    get_coords(soup1, project)  # Координаты Х и У записываются в словарь project

    write_webpage_to_html(id_object_name, html_obj,
                          'D:/PYTHON/NCA 03072017/WorkNew/WorkParsing/HTMLs')  # write web page to html file
    # get_photos(soup1, project, 'D:/PYTHON/2017/Parsing/WorkParsingNEW/Photos') # write object's photos from web page to local computer
    options_list = []  # Добавлен для того, чтобы исключать повторную обработку option если данный параметр встречается в тексте где-то еще
    for i in table:  # Проходимся по каждой строке на странице объявления
        for option in realt_fields_list:  # Прохдимся по каждому параметру из списка всевозможных параметров на странице. Спиосок создан из словаря соответстий поля на реалте и поля в ексель (Oficces_Realt_Excel).
            if option in i.text and not option in options_list:  # Если параметр есть в тексте, то начинаем его обрабатывать
                print(option)
                if not option in options_list:  # Добавлен для того, чтобы исключать повторную обработку option если данный параметр встречается в тексте где-то еще
                    options_list.append(option)
                realt_answer = i.text.split(option)[1].strip()  # Получаем только ответ
                Excel_field = Realt_Excel_dict[option]  # Получаем название поля в Excel

                if option == "Площадь":
                    project[Excel_field] = get_area(realt_answer)

                elif option == "Ориентировочная стоимость эквивалентна":
                    print(realt_answer)
                    # realt_answer = 1 677 руб/кв.м 1 677 руб/кв.м  Цена сделки определяется по соглашению сторон. Расчеты осуществляются в белорусских рублях в соответствии с законодательством Республики Беларусь.
                    get_finish_price(realt_answer, project, Excel_field)

                elif option == "Вид объекта":
                    Excel_field2 = Realt_Excel_dict['Вид объекта2']
                    Excel_field3 = Realt_Excel_dict['Вид объекта3']
                    get_finish_vid_object(realt_answer, project, Excel_field, Excel_field2, Excel_field3)

                elif option == "НДС":
                    try:
                        realt_answer = i.text.split(option)[
                            2].strip()  # потому что realt_answer гзначально такой список ['', ' ', ' не включен)'] Поэтому берем третий элемент (Также поменяла в json словаре Offices_Realt_Fields_Options.json
                        project[Excel_field] = Excel_options_dict[Excel_field][realt_answer]
                    except:  # Может быть что поля НДС нет на странице но строка "НДС встречается в тексте. Поэтому если она встречается то просто пропустить
                        pass
                elif option == "Телефоны":
                    get_contacts(realt_answer, project, Excel_field)
                elif option == "Вода":
                    Excel_field2 = Realt_Excel_dict['Вода2']
                    project[Excel_field] = Excel_options_dict[Excel_field][realt_answer]
                    project[Excel_field2] = Excel_options_dict[Excel_field2][realt_answer]
                elif option == "Высота потолков":
                    project[Excel_field] = get_hight(realt_answer)
                elif option == "Адрес":  # Никольская ул., 66-2, 40 лет Победы ул., 66-2,
                    Excel_field2 = Realt_Excel_dict['Адрес2']  # название улицы
                    Excel_field3 = Realt_Excel_dict['Адрес3']  # номер дома
                    Excel_field4 = Realt_Excel_dict['Адрес4']  # корпус
                    get_full_address(realt_answer, project, Excel_field, Excel_field2, Excel_field3, Excel_field4,
                                     id_object_name)
                elif option == "Район области":
                    project[Excel_field] = realt_answer.split('район')[0].strip()
                elif Realt_Excel_dict[option] in Excel_options_dict:
                    try:
                        project[Excel_field] = Excel_options_dict[Realt_Excel_dict[option]][realt_answer]
                    except KeyError:  # есть объявление https://realt.by/sale/shops/object/1106690/ у которого Материал стен не из классификатора
                        project[Excel_field] = '{} - не из классификатора'.format(realt_answer)
                else:
                    project[Realt_Excel_dict[option]] = realt_answer
    print(project)
    return project


def parse_page(html):
    soup = BeautifulSoup(html, "html.parser")
    # look for hrefs in titles
    table = soup.find_all('div', {'class': 'bd-item'}) # Получаем список с объявлениями на странице

    projects = [] # Список со словарями со страницы, где каждый словарь соответствует одному объявлению на странице. Словарь в таком виде, в котором будет записываться в Ексель
    # проходимся по каждому объявлению
    for row in table:
        # get hrefs of every page
        href_name = row.find('a')
        obj_url = href_name.get("href")
        project = {} # Для записи одного объявления в словарь
        parse_object(obj_url, project)
        projects.append(project)
    print(projects)
    return projects





html = get_html(baseurl)
# add_projects_into_existing_excel(parse_page(html), excel_path="MyExcel.xlsx")

add_project_into_existing_excel(parse_object(baseurl), excel_path = "MyExcel.xlsx")




soup = BeautifulSoup(html, "html.parser")
pages = soup.find('div', {'class': 'uni-paging'})
if pages:
    last_page = pages.text.split("... ")[1].strip()
    print(last_page)

    last_url = int(last_page) - 1
    # for i in range(1, int(last_page)):
    for i in range(4, 5):
        url = "{}?page={}".format(baseurl, i)
        print(url)
        html = get_html(url)
        add_projects_into_existing_excel(parse_page(html), excel_path="MyExcel.xlsx")
        the_last_succesful_page = 1
        print("The last succesful page is {}".format(i+1))
        waiting_time = random.randint(1, 10)
        print("Waiting time is {}".format(waiting_time))
        time.sleep(waiting_time)






