# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    imgs = scrapy.Field()
    title = scrapy.Field()
    subtitle = scrapy.Field()
    link = scrapy.Field()
    session = scrapy.Field()
    sub_session = scrapy.Field()
    author = scrapy.Field()
    publisher = scrapy.Field()
    text = scrapy.Field()
    date = scrapy.Field()
    hour = scrapy.Field()
    tags = scrapy.Field()
