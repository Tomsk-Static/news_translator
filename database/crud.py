from typing import List
from sqlalchemy.orm import Session
from . import alch_models
from news import models, download
import uuid

#################SOURCES##############################
def create_source(source: models.Source, db: Session):
    source.uuid = str(uuid.uuid4())
    db_source = alch_models.Source(**source.dict())
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return db_source


def get_sources(db: Session):
    return db.query(alch_models.Source).all()


def get_source(uuid: str, db: Session):
    return db.query(alch_models.Source).filter(alch_models.Source.uuid==uuid).first()

def delete_source(uuid: str, db: Session):
    db.query(alch_models.Article).filter(alch_models.Article.source_uuid==uuid).delete()
    db.query(alch_models.Category).filter(alch_models.Category.source_uuid==uuid).delete()
    db.query(alch_models.Source).filter(alch_models.Source.uuid==uuid).delete()
    db.commit()
    return uuid


def delete_sources_all(db: Session):
    db.query(alch_models.Article).delete()
    db.query(alch_models.Category).delete()
    db.query(alch_models.Source).delete()
    db.commit()
    return 'Success!'


def get_sources_categories(uuid: str, db: Session):
    db_categories = db.query(alch_models.Category).filter(alch_models.Category.source_uuid==uuid).all()
    return db_categories


def download_categories(uuid: str, db: Session):
    db_source = db.query(alch_models.Source).filter(alch_models.Source.uuid==uuid).first()
    categories = download.categories_download(url_source=db_source.url, uuid_source=db_source.uuid)
    db_categories = list([alch_models.Category(**category.dict()) for category in categories])
    db.add_all(db_categories)
    db.commit()
    return db_categories
    

#################CATEGORIES##############################

def get_category(uuid: str, db: Session):
    return db.query(alch_models.Category).filter(alch_models.Category.uuid==uuid).first()


def get_categories(db: Session):
    return db.query(alch_models.Category).all()


def create_category(category: models.Category, db: Session):
    category.uuid = str(uuid.uuid4())
    db_category = alch_models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(uuid: str, db: Session):
    db.query(alch_models.Article).filter(alch_models.Article.category_uuid==uuid).delete()
    db.query(alch_models.Category).filter(alch_models.Category.uuid==uuid).delete()
    db.commit()
    return uuid


def delete_categories_all(db: Session):
    db.query(alch_models.Article).delete()
    db.query(alch_models.Category).delete()
    db.commit()
    return 'Success!'


def get_categories_articles(uuid: str, db: Session):
    db_articles = db.query(alch_models.Article).filter(alch_models.Article.category_uuid==uuid).all()
    return db_articles


def download_articles(uuid: str, news_per_source: int, db: Session):
    db_category = db.query(alch_models.Category).filter(alch_models.Category.uuid==uuid).first()

    articles = download.articles_download(
        url_source=db_category.url,
        source_uuid=db_category.source_uuid,
        category_uuid=db_category.uuid,
        news_count=news_per_source
    )

    db_articles = list([alch_models.Article(**artic.dict()) for artic in articles])
    db.add_all(db_articles)
    db.commit()
    return db_articles

#################ARTICLES##############################

def get_articles(db: Session):
    return db.query(alch_models.Article).all()


def get_article(uuid: str, db: Session):
    db_article = db.query(alch_models.Article).filter(alch_models.Article.uuid==uuid).first()
    return db_article


def create_article(db: Session, article: models.Article):
    article.uuid = str(uuid.uuid4)
    db_article = alch_models.Article(**article.dict())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


def update_article(article: models.Article, db: Session):
    db_article = db.query(alch_models.Article).filter(alch_models.Article.uuid==article.uuid).first()

    for attr, val in vars(article).items():
        if getattr(db_article, attr) != val:
            setattr(db_article, attr, val)

    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


def create_article_pack(db: Session, articles: List[models.Article]):
    db_articles = list([alch_models.Article(**a.dict()) for a in articles])
    db.add_all(db_articles)
    db.commit()
    return db_articles


def delete_article(db: Session, uuid: str):
    db.query(alch_models.Article).filter(alch_models.Article.uuid==uuid).delete()
    db.commit()
    return uuid


def delete_articles_all(db: Session):
    db.query(alch_models.Article).filter().delete()
    db.commit()
    return 'Success!'
