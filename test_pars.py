from bs4 import BeautifulSoup
import requests
import urllib

html = requests.get('https://realt.by/sale/offices/object/1087691/')
with open('page_content.html', 'wb') as fid:
    fid.write(html.content)
