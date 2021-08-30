import alch_models
from database import engine

alch_models.Base.metadata.create_all(bind=engine)