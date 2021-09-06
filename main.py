
import uvicorn
from fastapi import FastAPI

from .routes import sources, categories, articles

from .database import alch_models

from .database.database import engine

alch_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(sources.app)
app.include_router(categories.app)
app.include_router(articles.app)


@app.get('/')
def root():
    return "{'message': 'hello'}"


# if __name__ == '__main__':
#     uvicorn.run(app)