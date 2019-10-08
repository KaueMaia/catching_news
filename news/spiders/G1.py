# -*- coding: utf-8 -*-
import scrapy
import time
import re
from datetime import datetime
from news.items import NewsItem
from news.models import list_links


class G1Spider(scrapy.Spider):
    name = 'G1'
    allowed_domains = ['g1.globo.com']
    start_urls = ['http://g1.globo.com/',
                  'https://g1.globo.com/economia/tecnologia/',
                  'https://g1.globo.com/ciencia-e-saude/',
                  'https://g1.globo.com/economia/agronegocios/',
                  'https://g1.globo.com/rj/rio-de-janeiro/',
                  'https://g1.globo.com/rj/norte-fluminense/',
                  'https://g1.globo.com/rj/regiao-dos-lagos/',
                  'https://g1.globo.com/rj/regiao-serrana/',
                  'https://g1.globo.com/rj/sul-do-rio-costa-verde/',
                  'https://g1.globo.com/sp/sao-paulo/']
    stop = 0

    def parse(self, response):
        for post in response.css(".feed-post"):
            if self.stop >= 10:
                break

            link = post.css(".feed-post-body-title a::attr(href)").extract_first()
            regex = re.compile(r'/ao-vivo/|/playlist/|/votacao/')
            if regex.search(link):
                continue
            if link not in list_links():
                yield response.follow(link, self.parse_news)
                time.sleep(3)

            next_page = response.css('.load-more ::attr(href)').extract_first()
            if next_page is not None and self.stop < 10:
                yield response.follow(next_page, self.parse)

    def parse_news(self, response):
        img, title, subtitle, link, session, sub_session, author, publisher, text, date, hour, tags = \
            None, None, None, None, None, None, None, None, None, None, None, None

        date, hour = response.css("time[itemprop='datePublished']::attr(datetime)").extract_first().split('T')
        hour = hour[:5]
        if datetime.strptime(date, '%Y-%m-%d').date() != datetime.now().date():
            self.stop += 1
            return None
        img = response.css(".content-media__image ::attr(data-src)").extract()
        title = " ".join([t.strip() for t in response.css(".title ::text").extract()]).strip()
        subtitle = " ".join([t.strip() for t in response.css(".subtitle ::text").extract()]).strip() if \
            response.css(".subtitle ::text").extract() else None
        link = response.url
        session = " ".join([t.strip() for t in response.css(".header-title ::text").extract()]).strip()
        sub_session = " ".join(t.strip() for t in response.css(".header-subtitle ::text").extract()).strip() if \
            response.css(".header-subtitle ::text").extract() else None
        author = response.css("span[itemprop='author'] meta::attr(content)").extract_first()
        publisher = response.css("span[itemprop='publisher'] meta::attr(content)").extract_first()
        text = " ".join(t.strip() for t in response.css(".content-text ::text").extract()).strip()

        news = NewsItem(link=link, title=title, subtitle=subtitle, session=session, sub_session=sub_session,
                        author=author, publisher=publisher, text=text, imgs=img, tags=tags, date=date, hour=hour)
        yield news
