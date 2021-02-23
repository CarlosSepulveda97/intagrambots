# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MemologoItem(scrapy.Item):

    
    likes = scrapy.Field()
    comments = scrapy.Field()
    src_img = scrapy.Field()

    pass
