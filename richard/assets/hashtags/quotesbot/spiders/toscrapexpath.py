# -*- coding: utf-8 -*-#run:     scrapy crawl toscrape-xpath -o quotes.json
import scrapy
from os import remove
from os import path



class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'toscrapexpath'
    start_urls = [
        'http://best-hashtags.com/hashtag/nature/',
    ]

    def parse(self, response):
        yield {
            'tags': response.xpath('/html/body/div[1]/div[3]/div/div/div[1]/div/div/div[1]/div[2]/p1/text()').extract(),
        }