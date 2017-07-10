import requests, json
from bs4 import BeautifulSoup

baseurl = 'https://realt.by/sale/shops/' # Базовый URL  - https://realt.by/sale/shops/

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


my_string = '23 460 руб, 260 руб/кв.м 23 460 руб, 260 руб/кв.м  Цена сделки определяется по соглашению сторон. Расчеты осуществляются в белорусских рублях в соответствии с законодательством Республики Беларусь.'

a = my_string.split(', ')[1].split(' ')[0]


# hanna = requests.get('http://www.nbrb.by/API/ExRates/Rates/145')
# print(hanna.content)

# n = b'{"Cur_ID":145,"Date":"2017-07-07T00:00:00","Cur_Abbreviation":"USD","Cur_Scale":1,"Cur_Name":"\xd0\x94\xd0\xbe\xd0\xbb\xd0\xbb\xd0\xb0\xd1\x80 \xd0\xa1\xd0\xa8\xd0\x90","Cur_OfficialRate":1.9714}'
# # print(str(n).split('"Cur_OfficialRate":')[1])
#
# data = json.loads(n)
# print(data['Cur_OfficialRate'])

b = '1 677'


    # elif u'\xa' in string:
    #     my_list = string.split(' ')
    #     new_string = '{}{}'.format(my_list[0], my_list[1])
    #     string = new_string
    #     return string

def get_html(url):
    try:
        res = requests.get(url, headers = headers)
    except requests.ConnectionError:
        return

    if res.status_code < 400:
        return res.content

def get_coords(i):
    string = i.text
    if 'ymaps' in string:
        coordinates = string.split('center: [')[1].split(']')[0]
        X = coordinates.split(', ')[0]
        Y = coordinates.split(', ')[1]

def parse(html):

    soup = BeautifulSoup(html, "html.parser")
    # print(soup.prettify())
    # look for hrefs in titles
    # table = soup.find('ymaps', {'src': '//api-maps.yandex.ru/2.0/?load=package.full&amp;lang=ru-RU" type="text/javascript'})
    table = soup.find_all('script', {'type': 'text/javascript'})
    # print(table)
    for i in table:

        string = i.text

        if 'ymaps' in string:
            coordinates = string.split('center: [')[1].split(']')[0]
            print(coordinates)
            X = coordinates.split(', ')[0]
            Y = coordinates.split(', ')[1]
            print(X)
            print(Y)



        # if 'ymaps' in i:
        #     print(i.text)
    # for i in table:
    #     print(i.text)
    #     b = i.find('ymaps')
    #     print('Here script where YMAPS exists {}'.format(b))
    # print("Скрипт равно {}".format(table))

html = get_html('https://realt.by/sale/shops/object/492168/')
parse(html)
