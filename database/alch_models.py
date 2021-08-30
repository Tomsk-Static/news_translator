from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship

from .database import Base

class Article(Base):
    __tablename__ = 'acrticle'

    uuid = Column(String(36), primary_key=True)
    title = Column(String(255))
    text = Column(Text(60000))
    source_uuid = Column(String(255), ForeignKey('source.uuid'))
    category_uuid = Column(String(255), ForeignKey('category.uuid'))
    publish_date = Column(DateTime)
    url = Column(String(255))


class Category(Base):
    __tablename__ = 'category'

    uuid = Column(String(36), primary_key=True)
    source_uuid = Column(String(36), ForeignKey('source.uuid'))
    url = Column(String(255))
    text = Column(String(255))


class Source(Base):
    __tablename__ = 'source'

    uuid = Column(String(36), primary_key=True)
    text = Column(String(255))
    url = Column(String(255))

