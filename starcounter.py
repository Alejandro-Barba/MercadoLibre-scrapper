from numpy import half
import requests
from bs4 import BeautifulSoup
from lxml import etree

#url = 'https://www.mercadolibre.com.mx/juego-de-mesa-scrabble-original-mattel/p/MLM7869188?pdp_filters=item_id:MLM946423073#searchVariation=MLM7869188&position=1&search_layout=stack&type=pad&tracking_id=0cdae0ba-cfdc-40d2-8a85-5187c4bb2fa3'
#url = 'https://articulo.mercadolibre.com.mx/MLM-899775020-foco-de-colores-rgbw-wifi-bombilla-inteligente-alexa-_JM?searchVariation=80348178724#searchVariation=80348178724&position=3&search_layout=stack&type=item&tracking_id=373df058-936a-4676-a371-bc62981bc8b3'
fstar = 'star_full'
hstar = 'star_half'
estar = 'star_empty'


def starcounter(url):
    r = requests.get(url)
    star_list = []
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        dom  = etree.HTML(str(soup))
        stars = dom.xpath("//div[@class='ui-pdp-header__info']//span[@class='ui-pdp-review__ratings']/*[name()='svg']/use")
        if stars:
            for star in stars:
                star_type = star.attrib['href'].replace('#','')
                star_list.append(star_type)
                full_stars = star_list.count(fstar)
                half_stars = star_list.count(hstar)
                real_stars = full_stars + (half_stars*.5)
        else :
            real_stars = 0
    else:
        print(r.status_code)
    return(str(real_stars))


#starcounter(url)