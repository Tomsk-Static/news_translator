from typing import List, Optional
from newspaper import build, news_pool
import uuid

def download_categories(source='https://www.bbc.com/news'):
    paper = build(source, memoize_articles=False)
    
    first_news = paper.articles[0]
    first_news.download()
    first_news.parse()




download_categories()
    