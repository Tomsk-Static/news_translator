from typing import List, Optional

from fastapi import Depends, APIRouter, HTTPException

from sqlalchemy.orm import Session

from ..database.database import SessionLocal

from ..crud import source_crud as crud

from ..news import models


app = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/source', response_model=models.SourceDb, tags=["Source"])
def create_source(source: models.SourceCreate, db: Session=Depends(get_db)):
    return crud.create_source(source=source, db=db)


@app.get('/sources', response_model=List[models.SourceDb], tags=["Source"])
def read_sources(db: Session=Depends(get_db)):
    return crud.get_sources(db=db)


@app.get('/source/{uuid}', response_model=models.SourceDb, tags=["Source"])
def read_source(uuid: str, db: Session=Depends(get_db)):
    return crud.get_source(uuid=uuid, db=db)


@app.delete('/source/{uuid}', tags=["Source"])
def delete_source(uuid: str, db: Session=Depends(get_db)):
    return crud.delete_source(uuid=uuid, db=db)


@app.delete('/sources', tags=["Source"])
def delete_sources_all(db: Session=Depends(get_db)):
    return crud.delete_sources(db=db)

@app.get('/source/categories/{uuid}', response_model=List[models.CategoryDb], tags=["Source"])
def get_sources_categories(uuid: str, db: Session=Depends(get_db)):
    return crud.get_sources_categories(uuid=uuid, db=db)


@app.post('/source/download/categories', response_model=List[models.CategoryDb], tags=["Source"])
def download_sources_categories(source_uuid: str, db: Session=Depends(get_db)):
    return crud.download_categories(uuid=source_uuid, db=db)