from newsapi import NewsApiClient
import os

PAGE_SIZE = 10
VALID_PARAMS = {'language', 'country', 'category', 'sources', 'page'}


def fetch_sources ():
    



def fetch_latest_news(query: str, **kwargs):
    """
    Fetch latest news headlines.
    """
    invalid_params = set(kwargs.keys()) - VALID_PARAMS
    if invalid_params:
        raise ValueError(f"Invalid parameters: {invalid_params}. Valid: {VALID_PARAMS}")
    
    news_api = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))
    return news_api.get_top_headlines(q=query, page_size=PAGE_SIZE,category= **kwargs)