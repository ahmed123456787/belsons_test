from newsapi import NewsApiClient
import os
from logging import getLogger

logger = getLogger(__name__)


def fetch_sources ():
    """
    Fetch news sources from NewsAPI.
    """
    try:
        logger.info("Fetching sources from NewsAPI...")
        news_api = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))

        sources =  news_api.get_sources().get('sources', [])
        logger.info(f"Fetched {len(sources)} sources from NewsAPI.")
        return sources
    except Exception as e:
        logger.error(f"Error fetching sources: {e}")
        return []
 


def fetch_latest_news(query: str = 'news', **kwargs):
    """
    Fetch latest news headlines.
    """
    try:
        news_api = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))
        result = news_api.get_everything(q=query, **kwargs)
        logger.info(f"Fetched news articles with query '{query}'")
        return result
    except Exception as e:
        logger.error(f"Error fetching latest news: {e}")
        return {'articles': [], 'totalResults': 0}