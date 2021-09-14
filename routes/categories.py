from typing import List, Optional

from fastapi import Depends, APIRouter, HTTPException

from sqlalchemy.orm import Session

from ..database.database import SessionLocal

from ..crud import category_crud as crud

from ..news import models

app = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/categories', response_model=List[models.CategoryDb], tags=["Category"])
def read_categories(db: Session=Depends(get_db)):
    return crud.get_categories(db=db)


@app.get('/category/{uuid}', response_model=models.CategoryDb, tags=["Category"])
def read_category(uuid: str, db: Session=Depends(get_db)):
    return crud.get_category(uuid=uuid, db=db)


@app.post('/category', response_model=models.CategoryDb, tags=["Category"])
def create_category(category: models.CategoryCreate, db: Session=Depends(get_db)):
    return crud.create_category(category=category, db=db)


@app.delete('/category/{uuid}', tags=["Category"])
def delete_category(uuid: str, db: Session=Depends(get_db)):
    return crud.delete_category(uuid=uuid, db=db)


@app.delete('/categories', tags=["Category"])
def delete_categories_all(db: Session=Depends(get_db)):
    return crud.delete_categories_all(db=db)


@app.get('/category/articles/{uuid}', response_model=List[models.ArticleDb], tags=["Category"])
def get_categories_articles(uuid: str, db: Session=Depends(get_db)):
    return crud.get_categories_articles(uuid=uuid, db=db)


@app.post('/category/download/articles', response_model=List[models.ArticleDb], tags=["Category"])
def download_categories_articles(download_articles: models.DownloadArticles, db: Session=Depends(get_db)):
    return crud.download_articles(uuid=download_articles.uuid.value, news_per_source=download_articles.count, db=db)