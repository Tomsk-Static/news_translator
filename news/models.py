from pydantic import BaseModel, HttpUrl, validator
from typing import Optional, List
from datetime import datetime

class Article(BaseModel):
    uuid: Optional[str]
    title: str
    text: Optional[str] = None
    source_uuid: Optional[str] = None
    category_uuid: Optional[str] = None
    publish_date: Optional[datetime] = datetime.now()
    url: Optional[str] = None

    # tell the Pydantic model to read the data even if it is not a dict, but an ORM model
    class Config:
        orm_mode = True
    
    @validator('publish_date')
    def set_currenttime(cls, publish_date):
        return publish_date or datetime.now()

class Articles(BaseModel):
    articles: List[Article]

    class Config:
        orm_mode = True


class Category(BaseModel):
    uuid: Optional[str]
    source_uuid: str
    text: str
    url: str

    class Config:
        orm_mode = True


class Source(BaseModel):
    uuid: Optional[str]
    url: str
    text: str

    class Config:
        orm_mode = True