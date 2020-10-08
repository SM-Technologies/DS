# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class Articulo(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    store = scrapy.Field()
    name = scrapy.Field()
    Price = scrapy.Field()
    description = scrapy.Field()
    link = scrapy.Field()
    imageURL = scrapy.Field()
