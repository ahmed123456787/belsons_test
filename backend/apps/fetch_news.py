from newsapi import NewsApiClient
import os
from .news_param_generator import sample_filters, build_query_combinations


def fetch_sources():
    """
    Fetch news sources from NewsAPI.
    """
    try:
        news_api = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))

        sources = news_api.get_sources().get('sources', [])
        return sources
    except Exception as e:
        return []


def fetch_top_headlines(countries=None, categories=None, sources=None, sample_countries=None, sample_categories=None, **kwargs):
    """
    Fetch latest news headlines with selective or sampled filtering.
    
    Args:
        countries (list): Specific country codes (e.g., ['us', 'fr'])
        categories (list): Specific category names (e.g., ['business', 'technology'])
        sources (list): Specific source IDs (e.g., ['bbc-news'])
        sample_countries (int): Randomly sample N countries (e.g., 4)
        sample_categories (int): Randomly sample N categories (e.g., 20)
        **kwargs: Additional parameters for custom queries
    
    Returns:
        dict: {'articles': [...], 'totalResults': count}
    """
    try:
        news_api = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))
        all_articles = []
        
        # Handle sampling
        if sample_countries or sample_categories:
            countries, categories = sample_filters(sample_countries, sample_categories)
        
        # If no filters provided, use custom kwargs only
        if not countries and not categories and not sources:
            result = news_api.get_top_headlines(**kwargs)
            return result
        
        # Build and execute queries for specified filters
        query_combinations = build_query_combinations(countries, categories, sources)
        
        for params in query_combinations:
            try:
                result = news_api.get_top_headlines(**params)
                articles = result.get('articles', [])
                all_articles.extend(articles)
            except Exception as e:
                continue
        
        # Remove duplicates based on URL
        unique_articles = {article['url']: article for article in all_articles}
        
        return {
            'articles': list(unique_articles.values()),
            'totalResults': len(unique_articles)
        }
    except Exception as e:
        return {'articles': [], 'totalResults': 0}