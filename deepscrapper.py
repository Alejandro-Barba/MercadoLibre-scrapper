import requests
from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd

testURL = 'https://articulo.mercadolibre.com.mx/MLM-830196557-foco-inteligente-led-8w-luz-rgbw-e27-tecnolite-connect-_JM?searchVariation=66322116261#searchVariation=66322116261&position=34&search_layout=grid&type=item&tracking_id=60c28aed-c590-43df-b82c-7947e818b3d9'

def deep(url_list):
    sales_list=[]
    for url in url_list:
        r = requests.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            sales = soup.find('span', attrs={'class': 'ui-pdp-subtitle'})
            sales = sales.text
            if sales == 'Nuevo':
                sales_list.extends(0)
            else :
                sales = int(sales.replace(' ','').split('|')[1].replace('vendidos',''))
                sales_list.extends(sales)
        else:
            print(r.status_code)