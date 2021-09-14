from pydantic import BaseModel, HttpUrl, validator
from typing import Optional, List
from datetime import datetime


class Uuid(BaseModel):
    value: str


class ArticleCreate(BaseModel):
    title: str
    text: Optional[str] = None
    source_uuid: str
    category_uuid: str
    publish_date: Optional[datetime] = datetime.now()
    url: str


class ArticleDb(ArticleCreate):
    uuid: str

    # tell the Pydantic model to read the data even if it is not a dict, but an ORM model
    class Config:
        orm_mode = True


class DownloadArticles(BaseModel):
    uuid: Uuid
    count: int


class CategoryCreate(BaseModel):
    source_uuid: str
    text: str
    url: str


class CategoryDb(CategoryCreate):
    uuid: str

    class Config:
        orm_mode = True


class SourceCreate(BaseModel):
    url: str
    text: str


class SourceDb(SourceCreate):
    uuid: str
    
    class Config:
        orm_mode = True
    