# -*- coding: utf-8 -*-
import scrapy
import time
import re
from datetime import datetime
from news.items import NewsItem
from news.models import list_links


class TecnoblogSpider(scrapy.Spider):
    name = 'Tecnoblog'
    allowed_domains = ['tecnoblog.net']
    start_urls = ['https://tecnoblog.net/',
                  'https://tecnoblog.net/categoria/news/',
                  'https://tecnoblog.net/categoria/especial/']
    stop = 0

    def parse(self, response):
        for article in response.css("article"):
            if self.stop >= 10:
                break

            link = article.css("div.texts h2 a::attr(href)").extract_first()
            if link not in list_links():
                yield response.follow(link, self.parse_article)
                time.sleep(3)

        next_page = response.css('a#mais::attr(href)').extract_first()
        if next_page is not None and self.stop < 10:
            yield response.follow("https://tecnoblog.net" + next_page, self.parse)

    def parse_article(self, response):
        img, title, subtitle, link, session, sub_session, author, publisher, text, date, hour, tags = \
            None, None, None, None, None, None, None, None, None, None, None, None

        date, hour = response.css("meta[property='article:published_time']::attr(content)").extract_first().split('T')
        hour = hour[:5]
        if datetime.strptime(date, '%Y-%m-%d').date() != datetime.now().date():
            self.stop += 1
            return None

        regex = re.compile(r'/uploads/')
        img = []
        for src in response.css("div[class^='entry'] img ::attr(src)").extract():
            if regex.search(src):
                img.append(src)
        link = response.url
        title = response.css("title ::text").extract_first()
        session = response.css("meta[property='article:section']::attr(content)").extract_first()
        author = response.css("span.author ::text").extract_first()
        text = " ".join([t.strip() for t in response.css("div.entry ::text").extract()]).strip()
        tags = response.css("meta[property='article:tag']::attr(content)").extract_first().split()

        news = NewsItem(link=link, title=title, subtitle=subtitle, session=session, sub_session=sub_session,
                        author=author, publisher=publisher, text=text, imgs=img, tags=tags, date=date, hour=hour)
        yield news
