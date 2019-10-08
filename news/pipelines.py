# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
from sqlalchemy.orm import sessionmaker
from news.models import db_connect, News, Imgs, Tags


def convert_datetime(date, time):
    date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    time = datetime.datetime.strptime(time, '%H:%M').time()
    return datetime.datetime.combine(date, time)


class NewsPipeline(object):

    def __init__(self):
        None

    def store_db(self, item):
        engine = db_connect()
        session = sessionmaker(bind=engine)
        session = session()
        news = News()

        imgs = []
        if item['imgs'] is not None:
            for img in item['imgs']:
                i = Imgs()
                i.img = img
                imgs.append(i)

        tags = []
        if item['tags'] is not None:
            for tag in item['tags']:
                t = Tags()
                t.tag = tag.lower()
                news.tags.append(t)

        news.link = item['link']
        news.title = item['title']
        news.subtitle = item['subtitle']
        news.session = item['session']
        news.sub_session = item['sub_session']
        news.author = item['author']
        news.publisher = item['publisher']
        news.text = item['text']
        news.imgs = imgs
        news.datetime = convert_datetime(item['date'], item['hour'])

        session.add(news)
        session.commit()
        session.close()

    def process_item(self, item, spider):
        self.store_db(item)
        return item
