from typing import List
from sqlalchemy.orm import Session
import uuid

from ..database import alch_models as orm
from ..news import models, download


def create_source(source: models.SourceCreate, db: Session):
    db_source = orm.Source(**source.dict(), uuid=str(uuid.uuid4()))
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return db_source


def get_sources(db: Session):
    db_sources = db.query(orm.Source).all()
    sources = list()

    for db_source in db_sources:
        source = models.SourceDb.from_orm(db_source)
        source.categories_count = db.query(orm.Category).filter(orm.Category.source_uuid==db_source.uuid).count()
        sources.append(source)

    return sources


def get_source(uuid: str, db: Session):
    return db.query(orm.Source).filter(orm.Source.uuid==uuid).first()


def delete_source(uuid: str, db: Session):
    db.query(orm.Article).filter(orm.Article.source_uuid==uuid).delete()
    db.query(orm.Category).filter(orm.Category.source_uuid==uuid).delete()
    db.query(orm.Source).filter(orm.Source.uuid==uuid).delete()
    db.commit()
    return uuid


def delete_sources_all(db: Session):
    db.query(orm.Article).delete()
    db.query(orm.Category).delete()
    db.query(orm.Source).delete()
    db.commit()
    return 'Success!'


def get_sources_categories(uuid: str, db: Session):
    db_categories = db.query(orm.Category).filter(orm.Category.source_uuid==uuid).all()
    categories = list()

    for db_category in db_categories:
        category = models.CategoryDb.from_orm(db_category)
        category.articles_count = db.query(orm.Article).filter(orm.Article.category_uuid==category.uuid).count()
        categories.append(category)

    return categories


def download_categories(uuid: str, db: Session):
    db_source = db.query(orm.Source).filter(orm.Source.uuid==uuid).first()
    categories = download.categories_download(url_source=db_source.url, uuid_source=db_source.uuid)
    db_categories = list([orm.Category(**category.dict()) for category in categories])
    db.add_all(db_categories)
    db.commit()
    return db_categories