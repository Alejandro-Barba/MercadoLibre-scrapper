from turtle import title
import requests
from bs4 import BeautifulSoup
from lxml import etree


def allproducts(product):
    title_list = []
    url_list = []
    prices_list = []
    images_url_list = []
    next_page = 'https://listado.mercadolibre.com.mx/'+product
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
    return title_list, images_url_list, url_list, prices_list


def limitedProducts(product, limit):
    title_list = []
    url_list = []
    prices_list = []
    images_url_list = []
    next_page = 'https://listado.mercadolibre.com.mx/'+product
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
        if len(title_list)>= int(limit):
            return title_list[:limit], images_url_list[:limit], url_list[:limit], prices_list[:limit]
        if first == last:
            break
        next_page = dom.xpath("//div[@class='ui-search-pagination']/ul/li[contains(@class,'--next')]/a")[0].get('href')
    return title_list, images_url_list, url_list, prices_list
