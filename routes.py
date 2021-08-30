from typing import List, Optional

import uvicorn

from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder

from news import models, download

from sqlalchemy.orm import Session

from database import crud, alch_models
from database.database import SessionLocal, engine

app = FastAPI()

# import alch_models
# from database import engine

alch_models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/source', response_model=models.Source)
def create_source(source: models.Source, db: Session=Depends(get_db)):
    return crud.create_source(source=source, db=db)


@app.get('/sources', response_model=List[models.Source])
def read_sources(db: Session=Depends(get_db)):
    return crud.get_sources(db=db)


@app.delete('/source/{uuid}')
def delete_source(uuid: str, db: Session=Depends(get_db)):
    return crud.delete_source(uuid=uuid, db=db)


@app.delete('/sources')
def delete_sources_all(db: Session=Depends(get_db)):
    return crud.delete_sources(db=db)

@app.get('/source/categories', response_model=List[models.Category])
def get_sources_categories(uuid: str, db: Session=Depends(get_db)):
    return crud.get_sources_categories(uuid=uuid, db=db)


@app.post('/source/download/categories', response_model=List[models.Category])
def download_sources_categories(source_uuid: str, db: Session=Depends(get_db)):
    return crud.download_categories(uuid=source_uuid, db=db)


@app.get('/categories', response_model=List[models.Category])
def read_categories(db: Session=Depends(get_db)):
    return crud.get_categories(db=db)


@app.get('/category/{uuid}', response_model=models.Category)
def read_category(uuid: str, db: Session=Depends(get_db)):
    return crud.get_category(uuid=uuid, db=db)


@app.post('/category', response_model=models.Category)
def create_category(category: models.Category, db: Session=Depends(get_db)):
    return crud.create_category(category=category, db=db)


@app.delete('/category')
def delete_category(uuid: str, db: Session=Depends(get_db)):
    return crud.delete_category(uuid=uuid, db=db)


@app.delete('/categories')
def delete_categories_all(db: Session=Depends(get_db)):
    return crud.delete_categories_all(db=db)


@app.get('/category/articles', response_model=List[models.Article])
def get_categories_articles(uuid: str, db: Session=Depends(get_db)):
    return crud.get_categories_articles(uuid=uuid, db=db)


@app.post('/category/download/articles', response_model=List[models.Article])
def download_categories_articles(category_uuid: str, count: int, db: Session=Depends(get_db)):
    return crud.download_articles(uuid=category_uuid, news_per_source=count, db=db)


@app.get('/articles', response_model=List[models.Article])
def read_articles(db: Session=Depends(get_db)):
    articles = crud.get_articles(db=db)
    return articles


@app.get('/article/{uuid}', response_model=models.Article)
def read_article(uuid: str, db: Session=Depends(get_db)):
    article = crud.get_article(db=db, uuid=uuid)
    return article


@app.post('/article/', response_model=models.Article)
def create_article(article: models.Article, db: Session=Depends(get_db)):
    return crud.create_article(db=db, article=article)


@app.delete('/article')
def delete_article(uuid: str, db: Session=Depends(get_db)):
    return crud.delete_article(db=db, uuid=uuid)


@app.delete('/articles')
def delete_article_all(db: Session=Depends(get_db)):
    return crud.delete_articles_all(db=db)


@app.patch('/article', response_model=models.Article)
def update_article(article: models.Article, db: Session=Depends(get_db)):
    return crud.update_article(article=article, db=db)
    

if __name__ == '__main__':
    uvicorn.run(app)