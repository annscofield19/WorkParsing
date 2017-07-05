from bs4 import BeautifulSoup
import requests
import pyexcel as pe
import xlwt
import openpyxl
import os
import json



baseurl = 'https://realt.by/sale/shops/?page=1' # Базовый URL  - https://realt.by/sale/shops/

with open('D:/PYTHON/2017/Parsing/WorkParsing/Offices_Realt_Excel', 'r', encoding='utf-8') as jf: #открываем файл на чтение
    Realt_Excel_dict = json.load(jf) # загружаем из файла данные в словарь Realt_Excel_dict = {'Вид объекта': 'Наименование', 'Вид объекта2': 'Назначение', 'Условия сделки': 'Тип предложения', ...
excel_fields_list = list(Realt_Excel_dict.values()) # Cоздаем лист с полями Ексель - ['Наименование', 'Назначение', 'Тип предложения', 'Контактные данные'...
realt_fields_list = list(Realt_Excel_dict.keys())

with open('D:/PYTHON/2017/Parsing/WorkParsing/Offices_Realt_Fields_Options', 'r', encoding='utf-8') as jf: #открываем файл на чтение
    Excel_options_dict = json.load(jf)

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
        # # write web page to html file
        # name_html ='{}.html'.format(id_object_name)
        # with open(name_html, 'wb') as file:
        #     file.write(html_obj)

        # # download photos
        # photos = soup1.find_all('div', {'class': 'photo-item'})
        # print(photos)
        # if photos:
        #     for photo in photos:
        #         print(photo)
        #         lnk = photo.find('img').get('src')
        #         print(lnk)
        #         nametemp = "{}_{}.jpeg".format(project['ID_object'], i)
        #         print(nametemp)
        #         i+=1
        #         with open(nametemp, "wb") as f:
        #             f.write(requests.get(lnk).content)


        for i in table:
            # Для объявлений, где есть координаты - для Общественно - деловой зоны их нет
            # if 'Координаты для онлайн карт' in i.text:
            #     coordinates = i.text.split('Координаты для онлайн карт')[1].strip()
            #     project['Xcoord'] = coordinates.split(' ')[0]
            #     project['Ycoord'] = coordinates.split(' ')[1]
            for option in realt_fields_list:
                if option in i.text:
                    print(option)
                    realt_answer = i.text.split(option)[1].strip()
                    if option == "Вид объекта":
                        # if "(" in realt_answer:
                        #     realt_answer = realt_answer.split(" (")[0]
                        # project[Realt_Excel_dict[option]] = Excel_options_dict[Realt_Excel_dict[option]][realt_answer]
                        print('Вид объекта не работает')
                    elif option == "НДС":
                        realt_answer = i.text.split(option)[2].strip() # потому что realt_answer гзначально такой список ['', ' ', ' не включен)'] Поэтому берем третий элемент (Также поменяла в json словаре Offices_Realt_Fields_Options
                        project[Realt_Excel_dict[option]] = Excel_options_dict[Realt_Excel_dict[option]][realt_answer]

                    elif option == "Телефоны":
                        if 'Пожалуйста, скажите что Вы нашли это объявление на сайте Realt.by' in i.text:
                            project[Realt_Excel_dict[option]] = realt_answer.split('Пожалуйста, скажите что Вы нашли это объявление на сайте Realt.by')[1].strip()
                        else:
                            project[Realt_Excel_dict[option]] = realt_answer
                    elif option == "Вода":
                        project[Realt_Excel_dict[option]] = Excel_options_dict[Realt_Excel_dict[option]][realt_answer]
                        project[Realt_Excel_dict['Вода2']] = Excel_options_dict[Realt_Excel_dict['Вода2']][realt_answer]
                    elif option == "Адрес": # Никольская ул., 66-2
                        if "." in realt_answer:
                            try:
                                a = realt_answer.split(".")[0] # Никольская ул
                                project[Realt_Excel_dict[option]] = a.split(' ')[1]
                                project[Realt_Excel_dict['Адрес2']] = a.split(' ')[0]
                            except IndexError:
                                print('No street')
                        if "," in realt_answer:
                            a = realt_answer.split(',')[1].strip()# 66-2
                            if "-" in a:
                                project[Realt_Excel_dict['Адрес3']] = a.split('-')[0]
                            else:
                                project[Realt_Excel_dict['Адрес3']] = a
                        if "-" in realt_answer:
                            project[Realt_Excel_dict['Адрес4']] = realt_answer.split('-')[1]

                    elif Realt_Excel_dict[option] in Excel_options_dict:
                        project[Realt_Excel_dict[option]] = Excel_options_dict[Realt_Excel_dict[option]][realt_answer]
                    else:
                        project[Realt_Excel_dict[option]] = realt_answer
        projects.append(project)
        print(project)
    # print(projects)

    # Write into NEW EXCEL. NOW NOT USED

    # wb = xlwt.Workbook()
    # ws = wb.add_sheet("Sheet")
    # row = 0
    # line = 0
    # for option in options:
    #     ws.write(row, line, option)
    #     line += 1
    # for project in projects:
    #     line = 0
    #     row += 1
    #     for option in options:
    #         if option in project:
    #             ws.write(row, line, project[option])
    #             line += 1
    # wb.save("D:/TESTYYYY.xls")

    # !!!! NOW USE - WRITE TO EXISTING EXCEL

    file = "MyExcel.xlsx"
    wb = openpyxl.load_workbook(filename=file)
    # Seleciono la Hoja
    ws = wb.get_sheet_by_name('Sheet')
    row_num = ws.max_row
    print(row_num)
    for project in projects:
        row_num += 1
        for i in range(1, 70):
            for field in excel_fields_list:
                if field == ws.cell(row=3, column=i).value and field in project:
                    ws.cell(row=row_num, column=i).value = project[field]
    wb.save(file)


html = get_html(baseurl)
parse(html)


# soup = BeautifulSoup(html, "html.parser")
# pages = soup.find('div', {'class': 'uni-paging'})
# last_page = pages.text.split("... ")[1].strip()
# print(last_page)
#
# last_url = int(last_page) - 1
# for i in range(1, last_url):
#     url = "{}?page={}".format(baseurl, i)
#     html = get_html(url)
#     parse(html)









