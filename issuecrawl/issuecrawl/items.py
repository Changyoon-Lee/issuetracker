# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IssuecrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    index = scrapy.Field()
    date = scrapy.Field()
    time = scrapy.Field()
    title = scrapy.Field()
    reply = scrapy.Field()
    views = scrapy.Field()
    pass
