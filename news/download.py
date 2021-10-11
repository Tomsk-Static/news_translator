from typing import List, Optional
from newspaper import build, news_pool
from .models import ArticleDb, CategoryDb
import uuid


def categories_download(url_source: str, uuid_source: str):
    paper = build(url_source, memoize_articles=False)
    categories = list()

    for category_url in paper.category_urls():
        category = CategoryDb(
            uuid = str(uuid.uuid4()),
            source_uuid = uuid_source,
            text = 'Category from {}'.format(url_source),
            url = category_url
        )
        categories.append(category)

    return categories


def articles_download(url_source: str, source_uuid: str, category_uuid: str, news_count: int):    
    paper = build(url_source, memoize_articles=False) 
    row_articles = paper.articles[:news_count]
    articles = list()

    for row_article in row_articles:
        row_article.download()
        row_article.parse()
        
        if row_article.title and row_article.text:
            article = ArticleDb(
                uuid = str(uuid.uuid4()),
                title = row_article.title,
                text = row_article.text,
                category_uuid = category_uuid,
                source_uuid = source_uuid,
                publish_date = row_article.publish_date,
                url = row_article.url
            )

            articles.append(article)

    return articles




    
