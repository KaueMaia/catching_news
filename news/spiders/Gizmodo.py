# -*- coding: utf-8 -*-
import scrapy
import re
import time
from datetime import datetime
from news.items import NewsItem
from news.models import list_links


class GizmodoSpider(scrapy.Spider):
    name = 'Gizmodo'
    allowed_domains = ['gizmodo.uol.com.br']
    start_urls = ['http://gizmodo.uol.com.br/']
    stop = 0

    def parse(self, response):
        for post in response.css(".layoutContent-main article"):
            if self.stop >= 10:
                break

            link = post.css("a::attr(href)").extract_first()
            if link not in list_links():
                yield response.follow(link, self.parse_news)
                time.sleep(3)

        next_page = response.css('.next ::attr(href)').extract_first()
        if next_page is not None and self.stop < 10:
            yield response.follow(next_page, self.parse)

    def parse_news(self, response):
        img, title, subtitle, link, session, sub_session, author, publisher, text, date, hour, tags = \
            None, None, None, None, None, None, None, None, None, None, None, None

        date, hour = response.css(".postSingle abbr::attr(content)").extract_first().split()
        hour = hour[:5]
        if datetime.strptime(date, '%Y-%m-%d').date() != datetime.now().date():
            self.stop += 1
            return None

        img = response.css(".postSingle img ::attr(src)").re(r"(https://giz.*)")
        title = response.css(".postSingle .postTitle ::text").extract_first()
        link = response.url
        session = response.css(".postSingle .postCategory ::text").extract_first()
        author = response.css(".postSingle .postMeta--author-author a::text").extract_first()
        text = " ".join([re.sub('window.uol.*?;|\xa0', ' ', text).strip()
                         for text in response.css(".postSingle .postContent :not([class^='foo_related_posts'])::text")
                        .extract()]).strip()
        tags = response.css(".postSingle .postTag ::text").extract()

        news = NewsItem(link=link, title=title, subtitle=subtitle, session=session, sub_session=sub_session,
                        author=author, publisher=publisher, text=text, imgs=img, tags=tags, date=date, hour=hour)
        yield news
