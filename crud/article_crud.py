from typing import List, Optional
from sqlalchemy.orm import Session
import uuid

from ..database import alch_models as orm
from ..news import models, download
from ..translator import translator as t


def get_articles(db: Session):
    return db.query(orm.Article).all()


def get_article(uuid: str, db: Session, dest_lang: Optional[str] = None):
    db_article = db.query(orm.Article).filter(orm.Article.uuid==uuid).first()
    if dest_lang:
        db_article.text = t.word_translate(text=db_article.text, dest=dest_lang)
    return db_article


def get_article_like_list(uuid: str, db: Session):
    db_article = db.query(orm.Article).filter(orm.Article.uuid==uuid).first()
    db_article.text = db_article.text.split()
    return db_article


def get_word_translate(word: str, dest_lang: str):
    return t.word_translate(text=word, dest_lang=dest_lang)


def create_article(article: models.ArticleCreate, db: Session):
    # article = str(uuid.uuid4)
    db_article = orm.Article(**article.dict(), uuid=str(uuid.uuid4()))
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


def update_article(article: models.ArticleCreate, db: Session):
    db_article = db.query(orm.Article).filter(orm.Article.uuid==article.uuid).first()

    for attr, val in vars(article).items():
        if getattr(db_article, attr) != val:
            setattr(db_article, attr, val)

    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


def create_article_pack(db: Session, articles: List[models.ArticleCreate]):
    db_articles = list([orm.Article(**a.dict(), uuid=str(uuid.uuid4())) for a in articles])
    db.add_all(db_articles)
    db.commit()
    return db_articles


def delete_article(uuid: str, db: Session):
    db.query(orm.Article).filter(orm.Article.uuid==uuid).delete()
    db.commit()
    return uuid


def delete_articles_all(db: Session):
    db.query(orm.Article).filter().delete()
    db.commit()
    return 'Success!'