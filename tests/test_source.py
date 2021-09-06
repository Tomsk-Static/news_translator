from fastapi.testclient import TestClient

from ..main import app

from ..news.models import Source, Category, Article

import uuid

from datetime import datetime

client = TestClient(app)

source_uuid = str(uuid.uuid4()) 
category_uuid = str(uuid.uuid4())
article_uuid = str(uuid.uuid4())


test_source = Source(
    uuid=source_uuid,
    text="Some test source",
    url="http://test_source.com"
    )

test_category = Category(
    uuid=category_uuid,
    source_uuid=source_uuid,
    text="Some test source",
    url="http://test_category.com"
    )

test_article = Article(
    uuid=article_uuid,
    title='Some test title',
    text='Some test text',
    source_uuid=source_uuid,
    category_uuid=category_uuid,
    publush_date=str(datetime.now()),
    url='Some test url'
)


def test_create_source():
    response = client.post('/source', json=test_source.dict())
    assert response.status_code == 200

def test_create_category():
    response = client.post('/category', json=test_category.dict())
    assert response.status_code == 200


def test_create_article():
    response = client.post('/article', json=test_article.dict())
    assert response.status_code == 200


def test_delete_article():
    response = client.delete('/article/{}'.format(article_uuid))
    assert response.status_code == 200


def test_delete_category():
    response = client.delete('/category/{}'.format(category_uuid))
    assert response.status_code == 200


def test_delete_source():
    response = client.delete('/source/{}'.format(source_uuid))
    assert response.status_code == 200


