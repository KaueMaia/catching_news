from sqlalchemy import create_engine, Column, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import (Integer, String, DateTime, Text)
from sqlalchemy.orm import sessionmaker

from scrapy.utils.project import get_project_settings

Base = declarative_base()


def db_connect():
    engine = create_engine('sqlite:///news.sqlite', encoding='utf-8')
    if not engine.dialect.has_table(engine, 'news'):
        create_table(engine)
    return engine


def create_table(engine):
    Base.metadata.create_all(engine)


def list_links():
    engine = db_connect()
    session = sessionmaker(bind=engine)
    session = session()
    news = session.query(News).all()
    links = []
    for notice in news:
        links.append(notice.link)
    return links


# class NewsTags(Base):
#     __tablename__ = 'News_Tags'
#     news_id = Column('news_id', Integer, ForeignKey('News.id'), primary_key=True)
#     tags_id = Column('tags_id', Integer, ForeignKey('Tags.id'), primary_key=True)
NewsTags = Table('News_Tags', Base.metadata,
                 Column('news_id', Integer, ForeignKey('News.id')),
                 Column('tags_id', Integer, ForeignKey('Tags.id')))


class News(Base):
    __tablename__ = "News"
    id = Column(Integer, primary_key=True, autoincrement=True)
    link = Column('link', String())
    title = Column('title', String())
    subtitle = Column('subtitle', String())
    session = Column('session', String())
    sub_session = Column('sub_session', String())
    author = Column('author', String())
    publisher = Column('publisher', String())
    text = Column('text', Text())
    imgs = relationship("Imgs")
    tags = relationship("Tags", secondary=NewsTags)
    datetime = Column('datetime', DateTime)


class Imgs(Base):
    __tablename__ = "Imgs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    img = Column('img', String())
    news_id = Column(Integer, ForeignKey('News.id'))


class Tags(Base):
    __tablename__ = "Tags"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tag = Column('tag', String())
    news = relationship("News", secondary=NewsTags)
