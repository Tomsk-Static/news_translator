
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import sources, categories, articles
from .database import alch_models
from .database.database import engine

alch_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    'http://localhost:8080'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(sources.app)
app.include_router(categories.app)
app.include_router(articles.app)


@app.get('/')
async def root():
    return "{'message': 'hello'}"


# if __name__ == '__main__':
#     uvicorn.run(app)