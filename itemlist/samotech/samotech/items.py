# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class Articulo(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    tienda = scrapy.Field()
    nombre = scrapy.Field()
    precio = scrapy.Field()
    descripcion = scrapy.Field()
    url = scrapy.Field()
    img = scrapy.Field()
