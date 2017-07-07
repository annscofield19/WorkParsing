import requests, json

baseurl = 'https://realt.by/sale/shops/object/1118514' # Базовый URL  - https://realt.by/sale/shops/

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

n = b'{"Cur_ID":145,"Date":"2017-07-07T00:00:00","Cur_Abbreviation":"USD","Cur_Scale":1,"Cur_Name":"\xd0\x94\xd0\xbe\xd0\xbb\xd0\xbb\xd0\xb0\xd1\x80 \xd0\xa1\xd0\xa8\xd0\x90","Cur_OfficialRate":1.9714}'
# print(str(n).split('"Cur_OfficialRate":')[1])

data = json.loads(n)
print(data['Cur_OfficialRate'])