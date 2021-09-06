from typing import List, Optional

from fastapi import Depends, APIRouter, HTTPException

from sqlalchemy.orm import Session

from ..database.database import SessionLocal

from ..crud import article_crud as crud

from ..news import models

app = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/articles', response_model=List[models.ArticleDb], tags=["Article"])
def read_articles(db: Session=Depends(get_db)):
    return crud.get_articles(db=db)
    

@app.get('/article/{uuid}', response_model=models.ArticleDb, tags=["Article"])
def read_article(uuid: str, db: Session=Depends(get_db)):
    return crud.get_article(uuid=uuid, db=db)
     

@app.post('/article', response_model=models.ArticleDb, tags=["Article"])
def create_article(article: models.ArticleCreate, db: Session=Depends(get_db)):
    return crud.create_article(article=article, db=db)


@app.delete('/article/{uuid}', tags=["Article"])
def delete_article(uuid: str, db: Session=Depends(get_db)):
    return crud.delete_article(uuid=uuid, db=db)


@app.delete('/articles', tags=["Article"])
def delete_article_all(db: Session=Depends(get_db)):
    return crud.delete_articles_all(db=db)


@app.patch('/article', response_model=models.ArticleDb, tags=["Article"])
def update_article(article: models.ArticleCreate, db: Session=Depends(get_db)):
    return crud.update_article(article=article, db=db)