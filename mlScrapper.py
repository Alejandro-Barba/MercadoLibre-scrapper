from turtle import title
import requests
from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd
from scrapper import deppScrapper
from excelSaver import imageAdder
#from PIL import Image

#uncomment next lines in production
""" print('Escribe lo que deseas buscar')
searchTerm = input('> ')
print(f'Buscando: {searchTerm}')
searchTerm = searchTerm.replace(' ','-') """

base_url = 'https://listado.mercadolibre.com.mx/'
new_items_filter = "_ITEM*CONDITION_2230284_NoIndex_True#applied_filter_id%3DITEM_CONDITION%26applied_filter_name%3DCondición%26applied_filter_order%3D9%26applied_value_id%3D2230284%26applied_value_name%3DNuevo%26applied_value_order%3D1%26applied_value_results%3D78%26is_custom%3Dfalse"

#uncomment next line in production
#r = requests.get(f'{base_url}+{searchTerm}+{new_items_filter}')
r = requests.get('https://listado.mercadolibre.com.mx/here-i-stand')
#Status code must be 200
print('status:', r.status_code)
soup = BeautifulSoup(r.content, 'html.parser')

#Start getting atributes in the search page

titles = soup.find_all('h2', attrs={'class': 'ui-search-item__title'})
titles = [i.text for i in titles]
print('titles:', len(titles))

""" urls = soup.find_all('a', attrs={'class':'ui-search-result__image'})
urls = [i.get('href') for i in urls]
print('url´s:',  len(urls)) """

#create a dom element with etree to use the Xpath and find difficult elements
dom  = etree.HTML(str(soup))

urls = dom.xpath("//li[@class='ui-search-layout__item']//div[@class='ui-search-result__image']//a[@class='ui-search-link']")
print('urls:',  len(urls))
urls = [i.attrib['href'] for i in urls]

prices = dom.xpath("//li[@class='ui-search-layout__item']//div[@class='ui-search-result__content-wrapper']//div[@class='ui-search-item__group__element ui-search-price__part-without-link']//div[@class='ui-search-price__second-line']//span[@class='price-tag-fraction']")
print('prices:',  len(prices))
prices = [int(i.text.replace(',','')) for i in prices]

images_url = dom.xpath("//li[@class='ui-search-layout__item']//div[@class='ui-search-result__image']//div[@class='slick-track']//img[1]")
images_url = [i.attrib['data-src'] for i in images_url]
print('image url´s:', len(images_url))

# use this two prints to check if you are getting the correct urls
# print(dir(images_url[0]))
#print(images_url[0].attrib)
#print(images_url[0].attrib['data-src'])

#Create a dataset and extract it to excel
df = pd.DataFrame({"titulos":titles, "img": images_url, "url":urls, "precios": prices} )
df = df.set_index('titulos')

with pd.ExcelWriter('DataFrame.xlsx') as writer:
    df.to_excel(writer, sheet_name='database')

next_page = dom.xpath("//div[@class='ui-search-pagination']/ul/li[contains(@class,'--next')]/a")[0].get('href')


first = int(soup.find('span', attrs={'class':'andes-pagination__link'}).text)
last = int(soup.find('li', attrs={'class':'andes-pagination__page-count'}).text.replace('de ',''))

""" r = requests.get(next_page)
if r.status_code == 200 :
    soup = BeautifulSoup(r.content, 'html.parser')
    first = int(soup.find('span', attrs={'class':'andes-pagination__link'}).text)
    print(first)
    next_page = dom.xpath("//div[@class='ui-search-pagination']/ul/li[contains(@class,'--next')]/a")[0].get('href')
    print(next_page)
 """
title_list = []
url_list = []
prices_list = []
images_url_list = []

next_page = 'https://listado.mercadolibre.com.mx/here-i-stand_ITEM*CONDITION_2230284_NoIndex_True#applied_filter_id%3DITEM_CONDITION%26applied_filter_name%3DCondici%C3%B3n%26applied_filter_order%3D11%26applied_value_id%3D2230284%26applied_value_name%3DNuevo%26applied_value_order%3D1%26applied_value_results%3D77%26is_custom%3Dfalse'
while True:
    r = requests.get(next_page)
    if r.status_code == 200 :
        soup = BeautifulSoup(r.content, 'html.parser')
        dom  = etree.HTML(str(soup))
        #titles
        titles = soup.find_all('h2', attrs={'class': 'ui-search-item__title'})
        titles = [i.text for i in titles]
        title_list.extend(titles)
        #urls
        urls = dom.xpath("//li[@class='ui-search-layout__item']//div[@class='ui-search-result__image']//a[@class='ui-search-link']")
        urls = [i.attrib['href'] for i in urls]
        url_list.extend(urls)
        #prices
        prices = dom.xpath("//li[@class='ui-search-layout__item']//div[@class='ui-search-result__content-wrapper']//div[@class='ui-search-item__group__element ui-search-price__part-without-link']//div[@class='ui-search-price__second-line']//span[@class='price-tag-fraction']")
        prices = [int(i.text.replace(',','')) for i in prices]
        prices_list.extend(prices)
        #images_url
        images_url = dom.xpath("//li[@class='ui-search-layout__item']//div[@class='ui-search-result__image']//div[@class='slick-track']//img[1]")
        images_url = [i.attrib['data-src'] for i in images_url]
        images_url_list.extend(images_url)
        first = int(soup.find('span', attrs={'class':'andes-pagination__link'}).text)
        last = int(soup.find('li', attrs={'class':'andes-pagination__page-count'}).text.replace('de ',''))

    else:
        break
    print('Escaneando página:',first, ' de ', last)

    if first == last:
        break
    next_page = dom.xpath("//div[@class='ui-search-pagination']/ul/li[contains(@class,'--next')]/a")[0].get('href')



df = pd.DataFrame({"titulo":title_list, "img": images_url_list, "url":url_list, "precios": prices_list} )
df = df.set_index('titulo')

with pd.ExcelWriter('DataFrame.xlsx') as writer:
    df.to_excel(writer, sheet_name='database')
    print('Archivo inicial guardado')

#print(deppScrapper(url_list))
def deepScraping(url_list,limit):
    #initialize the deep scrapper for the urls and the limit establiches by the user
    url_list_limited = url_list[:limit-1]
    title_list ,image_url_list , image_qty_list , sales_list , pdp_url_list , stars_list , reviews_list , not_discount_price_list , discount_price_list , brand_list , sku_list , char3_list , char4_list , char5_list , char6_list , char7_list , questions_list , seller_list , seller_status_list , seller_sales_60_days_list = deppScrapper(url_list_limited)
    df2 = pd.DataFrame({"Titulo" : title_list, "Imagen" : image_url_list, "Vendidos" : sales_list, "URL" : pdp_url_list, "Estrellas" : stars_list, "Reseñas" : reviews_list, "Precio inicial" : not_discount_price_list, "Precio con descuento" : discount_price_list, "Marca" : brand_list, "SKU" : sku_list, "Característica 1" : char3_list,  "Característica 2" : char4_list,  "Característica 3" : char5_list,  "Característica 4" : char6_list,  "Característica 5" : char7_list, "Cantidad de preguntas" : questions_list , "Vendedor" : seller_list , "Estatus del vendedor" : seller_status_list , "Ventas del vendedor en ultimos 60 días" : seller_sales_60_days_list })
    df2 = df2.set_index('Titulo')
    with pd.ExcelWriter('DeepScrapping.xlsx') as writer:
        df2.to_excel(writer, sheet_name='database')
        print('Archivo completo guardado')
#deepScraping(url_list, 10)

def excelFormater(title_list):
    print('Iniciando formato de archivo')
    imageAdder(len(title_list)+2)

excelFormater(title_list)