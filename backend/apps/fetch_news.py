from newsapi import NewsApiClient
import os
from logging import getLogger
from .news.models import Country, Category
import random

logger = getLogger(__name__)


def fetch_sources():
    """
    Fetch news sources from NewsAPI.
    """
    try:
        logger.info("Fetching sources from NewsAPI...")
        news_api = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))

        sources = news_api.get_sources().get('sources', [])
        logger.info(f"Fetched {len(sources)} sources from NewsAPI.")
        return sources
    except Exception as e:
        logger.error(f"Error fetching sources: {e}")
        return []


def _sample_filters(countries_count=None, categories_count=None):
    """
    Randomly sample countries and categories from database.
    
    Args:
        countries_count (int): Number of countries to sample (None = all)
        categories_count (int): Number of categories to sample (None = all)
    
    Returns:
        tuple: (countries_list, categories_list)
    """
    # Get all available countries and categories
    all_countries = list(Country.objects.values_list('code', flat=True))
    all_categories = list(Category.objects.values_list('name', flat=True))
    
    # Sample or use all
    sampled_countries = random.sample(all_countries, min(countries_count or len(all_countries), len(all_countries)))
    sampled_categories = random.sample(all_categories, min(categories_count or len(all_categories), len(all_categories)))
    
    logger.info(f"Sampled {len(sampled_countries)} countries: {sampled_countries}")
    logger.info(f"Sampled {len(sampled_categories)} categories: {sampled_categories}")
    
    return sampled_countries, sampled_categories


def _build_query_combinations(countries=None, categories=None, sources=None):
    """
    Build query parameter combinations based on provided filters.
    
    Args:
        countries (list): Specific country codes (e.g., ['us', 'fr'])
        categories (list): Specific category names (e.g., ['business', 'technology'])
        sources (list): Specific source IDs (e.g., ['bbc-news'])
    
    Returns:
        list: List of query parameter dictionaries
    """
    combinations = []
    
    # If countries and categories provided, create combinations
    if countries and categories:
        for country in countries:
            for category in categories:
                combinations.append({
                    'country': country,
                    'category': category,
                    'page_size': 100
                })
    
    # If only countries provided
    elif countries:
        for country in countries:
            combinations.append({
                'country': country,
                'page_size': 100
            })
    
    # If only categories provided
    elif categories:
        for category in categories:
            combinations.append({
                'category': category,
                'page_size': 100
            })
    
    # If sources provided
    if sources:
        for source in sources:
            combinations.append({
                'sources': source,
                'page_size': 100
            })
    
    logger.info(f"Built {len(combinations)} query combinations")
    return combinations


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
            countries, categories = _sample_filters(sample_countries, sample_categories)
        
        # If no filters provided, use custom kwargs only
        if not countries and not categories and not sources:
            result = news_api.get_top_headlines(**kwargs)
            logger.info("Fetched headlines with custom query")
            return result
        
        # Build and execute queries for specified filters
        query_combinations = _build_query_combinations(countries, categories, sources)
        
        for params in query_combinations:
            try:
                result = news_api.get_top_headlines(**params)
                articles = result.get('articles', [])
                all_articles.extend(articles)
                logger.info(f"Fetched {len(articles)} articles with params: {params}")
            except Exception as e:
                logger.warning(f"Error fetching with params {params}: {e}")
                continue
        
        # Remove duplicates based on URL
        unique_articles = {article['url']: article for article in all_articles}
        logger.info(f"Total unique articles fetched: {len(unique_articles)}")
        
        return {
            'articles': list(unique_articles.values()),
            'totalResults': len(unique_articles)
        }
    except Exception as e:
        logger.error(f"Error fetching latest news: {e}")
        return {'articles': [], 'totalResults': 0}