from typing import List
from sqlalchemy.orm import Session
import uuid

from ..database import alch_models as orm
from ..news import models, download


def get_category(uuid: str, db: Session):
    return db.query(orm.Category).filter(orm.Category.uuid==uuid).first()


def get_categories(db: Session):
    return db.query(orm.Category).all()


def create_category(category: models.CategoryCreate, db: Session):
    db_category = orm.Category(**category.dict(), uuid=str(uuid.uuid4()))
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(uuid: str, db: Session):
    db.query(orm.Article).filter(orm.Article.category_uuid==uuid).delete()
    db.query(orm.Category).filter(orm.Category.uuid==uuid).delete()
    db.commit()
    return uuid


def delete_categories_all(db: Session):
    db.query(orm.Article).delete()
    db.query(orm.Category).delete()
    db.commit()
    return 'Success!'


def get_categories_articles(uuid: str, db: Session):
    db_articles = db.query(orm.Article).filter(orm.Article.category_uuid==uuid).all()
    return db_articles


def download_articles(uuid: str, news_per_source: int, db: Session):
    db_category = db.query(orm.Category).filter(orm.Category.uuid==uuid).first()

    articles = download.articles_download(
        url_source=db_category.url,
        source_uuid=db_category.source_uuid,
        category_uuid=db_category.uuid,
        news_count=news_per_source
    )

    db_articles = list([orm.Article(**artic.dict()) for artic in articles])
    db.add_all(db_articles)
    db.commit()
    return db_articles