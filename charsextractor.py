from email import charset
from numpy import half
import requests
from bs4 import BeautifulSoup
from lxml import etree

url = 'https://articulo.mercadolibre.com.mx/MLM-832287799-lampara-industrial-de-iluminacion-para-el-hogar-e26-e27-3-_JM?searchVariation=66742377786#searchVariation=66742377786&position=2&search_layout=stack&type=item&tracking_id=ac48b26c-ca32-4c48-9269-7c71796753d7'
#url = 'https://articulo.mercadolibre.com.mx/MLM-899775020-foco-de-colores-rgbw-wifi-bombilla-inteligente-alexa-_JM?searchVariation=80348178724#searchVariation=80348178724&position=3&search_layout=stack&type=item&tracking_id=373df058-936a-4676-a371-bc62981bc8b3'



def charextractor(url):
    brand_list=[]
    sku_list=[]
    char3_list=[]
    char4_list=[]
    char5_list=[]
    char6_list=[]
    char7_list=[]
    r = requests.get(url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        dom  = etree.HTML(str(soup))
        chars = dom.xpath("(//div[@class='ui-pdp-collapsable__container']//div[@class='ui-vpp-striped-specs__table'])[1]//tbody[@class='andes-table__body']//span[@class='andes-table__column--value']")
        if chars:
            if len(chars) > 0:
                brand = chars[0].text
            else :
                brand = 'No disponible'
            if len(chars) > 1:
                sku = chars[1].text
            else :
                sku = 'No disponible'
            if len(chars) > 2:
                char3 = chars[2].text
            else:
                char3 = 'No disponible'
            if len(chars) > 3:
                char4 = chars[3].text
            else:
                char4 = 'No disponible'
            if len(chars) > 4:
                char5 = chars[4].text
            else:
                char5 = 'No disponible'
            if len(chars) > 5:
                char6= chars[5].text
            else:
                char6 = 'No disponible'
            if len(chars) > 6:
                char7 = chars[6].text
            else:
                char7 = 'No disponible'
        else :
            brand = 'No disponible'
            sku = 'No disponible'
            char3 = 'No disponible'
            char4 = 'No disponible'
            char5 = 'No disponible'
            char6 = 'No disponible'
            char7 = 'No disponible'
        brand_list.append(brand)
        sku_list.append(sku)
        char3_list.append(char3)
        char4_list.append(char4)
        char5_list.append(char5)
        char6_list.append(char6)
        char7_list.append(char7)
    else:
        print(r.status_code)
    return(brand_list , sku_list , char3_list , char4_list , char5_list, char6_list , char7_list)


charextractor(url)