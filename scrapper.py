from operator import not_
import requests
from bs4 import BeautifulSoup
from lxml import etree
from starcounter import starcounter
from charsextractor import charextractor

#url_list = ['https://articulo.mercadolibre.com.mx/MLM-866114578-kit-3-focos-inteligentes-led-8w-atenuable-colors-tecnolite-_JM?searchVariation=73746794283#searchVariation=73746794283&position=2&search_layout=grid&type=item&tracking_id=8af1ab12-e192-4677-ae45-2a396250edb8' ,'https://articulo.mercadolibre.com.mx/MLM-1303651051-foco-led-inteligente-rgbcw-wifi-9w-con-mando-a-distancia-e27-_JM#searchVariation=173570399031&position=1&search_layout=stack&type=pad&tracking_id=b94d49e9-2dc5-4d8f-b2f0-75fce0afb34c&is_advertising=true&ad_domain=VQCATCORE_LST&ad_position=1&ad_click_id=NzgxZmQ3OWQtNjc1MC00MDVkLWFiZjItZTJjMzcyYTAwYjdh','https://articulo.mercadolibre.com.mx/MLM-899775020-foco-de-colores-rgbw-wifi-bombilla-inteligente-alexa-_JM?searchVariation=80348178724#searchVariation=80348178724&position=3&search_layout=stack&type=item&tracking_id=373df058-936a-4676-a371-bc62981bc8b3','https://articulo.mercadolibre.com.mx/MLM-832287799-lampara-industrial-de-iluminacion-para-el-hogar-e26-e27-3-_JM?searchVariation=66742377786#searchVariation=66742377786&position=2&search_layout=stack&type=item&tracking_id=ac48b26c-ca32-4c48-9269-7c71796753d7']

def deppScrapper(url_list):
    title_list=[]
    image_url_list=[]
    image_qty_list =[]
    sales_list=[]
    pdp_url_list=[]
    stars_list=[]
    reviews_list=[]
    discount_price_list=[]
    not_discount_price_list=[]
    brand_list=[]
    sku_list=[]
    char3_list=[]
    char4_list=[]
    char5_list=[]
    char6_list=[]
    char7_list=[]
    questions_list=[]
    seller_list=[]
    seller_status_list=[]
    seller_sales_60_days_list = []
    print('Initializing deep scrapping')

    for url in url_list:
        r = requests.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            dom  = etree.HTML(str(soup))
            sales = soup.find('span', attrs={'class': 'ui-pdp-subtitle'})
            sales = sales.text
            title = soup.find('h1', attrs={'class': 'ui-pdp-title'})
            title = title.text
            title_list.append(title)
            images_url = dom.xpath("//div[@class='ui-pdp-gallery']//span[@class='ui-pdp-gallery__wrapper'][1]//figure[@class='ui-pdp-gallery__figure']//img[1]")
            images_url = images_url[0].attrib['data-zoom']
            image_url_list.append(images_url)
            image_qty = dom.xpath("//div[@class='ui-pdp-gallery']//span[@class='ui-pdp-gallery__wrapper']//figure[@class='ui-pdp-gallery__figure']")
            image_qty = len(image_qty)
            image_qty_list.append(image_qty)
            pdp_url_list.append(url)
            review = soup.find('span', attrs={'class':'ui-pdp-review__amount'})
            if review:
                review = review.text.replace(' opiniones','')
            else:
                review = '0'
            reviews_list.append(review)
            not_disc_price = dom.xpath("//div[@class='ui-pdp-price__second-line']//span[@class='andes-money-amount__fraction']")
            not_disc_price = not_disc_price[0].text.replace(',', '')
            not_discount_price_list.append(not_disc_price)
            disc_price = dom.xpath("//s[contains(@class,'ui-pdp-price__original-value')]//span[@class='andes-money-amount__fraction']")
            if disc_price:
                disc_price = disc_price[0].text.replace(',', '')
            else :
                disc_price = not_disc_price
            discount_price_list.append(disc_price)
            chars = charextractor(url)
            brand_list.append(chars[0][0])
            sku_list.append(chars[1][0])
            char3_list.append(chars[2][0])
            char4_list.append(chars[3][0])
            char5_list.append(chars[4][0])
            char6_list.append(chars[5][0])
            char7_list.append(chars[6][0])
            question = dom.xpath("//div[@class='ui-pdp-qadb__questions-list']//div[@class='ui-pdp-qadb__questions-list__wraper']//div[@class='ui-pdp-qadb__questions-list__question']")
            questions_list.append(len(question))
            seller = dom.xpath("//div[@class='ui-seller-info']//div[@class='ui-pdp-seller__header__title']")
            if seller:
                seller = seller[0].text
            else:
                seller = 'No disponible'
            seller_list.append(seller)
            seller_status = dom.xpath("//div[@class='ui-seller-info']//p[@class='ui-seller-info__status-info__title ui-pdp-seller__status-title']")
            if seller_status :
                seller_status = seller_status[0].text
            else :
                seller_status = 'No existe información'
            seller_status_list.append(seller_status)
            seller_sales = dom.xpath("//div[@class='ui-seller-info']//strong[@class='ui-pdp-seller__sales-description']")
            if seller_sales:
                seller_sales = seller_sales[0].text
            else :
                seller_sales = '0'
            seller_sales_60_days_list.append(seller_sales)
            print(f'Obteniendo ' + str(url_list.index(url)+1) + ' de ' + str(len(url_list)))
            print(title)
            
            stars_list.append(starcounter(url))
            if sales == 'Nuevo':
                sales_list.append('0')
            else :
                sales = sales.replace(' ','').split('|')[1].replace('vendidos','').replace('vendido','')
                sales_list.append(sales)
            
        else:
            print(r.status_code)
    print('Deep scrapper finished succesfully!')

    return title_list ,image_url_list , image_qty_list , sales_list , pdp_url_list , stars_list , reviews_list , not_discount_price_list , discount_price_list , brand_list , sku_list , char3_list , char4_list , char5_list , char6_list , char7_list , questions_list , seller_list , seller_status_list , seller_sales_60_days_list

#deppScrapper(url_list)