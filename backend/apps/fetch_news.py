from newsapi import NewsApiClient
import os
from logging import getLogger

logger = getLogger(__name__)

PAGE_SIZE = 10
VALID_PARAMS = {'language', 'country', 'category', 'sources', 'page'}



def fetch_sources ():
    try:
        logger.info("Fetching sources from NewsAPI...")
        news_api = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))

        sources =  news_api.get_sources().get('sources', [])
        logger.info(f"Fetched {len(sources)} sources from NewsAPI.")
        return sources
    except Exception as e:
        return []



def fetch_latest_news(query: str, **kwargs):
    """
    Fetch latest news headlines.
    """
    invalid_params = set(kwargs.keys()) - VALID_PARAMS
    if invalid_params:
        raise ValueError(f"Invalid parameters: {invalid_params}. Valid: {VALID_PARAMS}")
    
    news_api = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))
    return news_api.get_top_headlines(q=query, page_size=PAGE_SIZE, **kwargs)