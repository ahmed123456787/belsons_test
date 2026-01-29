from newsapi import NewsApiClient
import os
from .news_param_generator import sample_filters, build_query_combinations
import logging

logger = logging.getLogger(__name__)


def fetch_sources():
    """
    Fetch news sources from NewsAPI.
    """
    try:
        logger.info("Starting fetch_sources...", os.getenv("NEWS_API_KEY"))
        news_api = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))

        logger.debug("Calling NewsAPI get_sources endpoint")
        sources = news_api.get_sources().get('sources', [])
        logger.info(f"Successfully fetched {len(sources)} sources from NewsAPI")
        return sources
    except Exception as e:
        logger.error(f"Error fetching sources: {str(e)}", exc_info=True)
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
        logger.info("Starting fetch_top_headlines...")
        logger.debug(f"Parameters - countries: {countries}, categories: {categories}, sources: {sources}, "
                    f"sample_countries: {sample_countries}, sample_categories: {sample_categories}")
        
        news_api = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))
        all_articles = []
        
        # Handle sampling
        if sample_countries or sample_categories:
            logger.info(f"Sampling filters - countries: {sample_countries}, categories: {sample_categories}")
            countries, categories = sample_filters(sample_countries, sample_categories)
            logger.info(f"Sampled {len(countries)} countries: {countries}")
            logger.info(f"Sampled {len(categories)} categories: {categories}")
        
        # If no filters provided, use custom kwargs only
        if not countries and not categories and not sources:
            logger.info("No specific filters provided, using custom kwargs")
            logger.debug(f"Custom kwargs: {kwargs}")
            result = news_api.get_top_headlines(**kwargs)
            articles_count = len(result.get('articles', []))
            logger.info(f"Fetched {articles_count} articles with custom parameters")
            return result
        
        # Build and execute queries for specified filters
        logger.info("Building query combinations...")
        query_combinations = build_query_combinations(countries, categories, sources)
        logger.info(f"Generated {len(query_combinations)} query combinations")
        logger.debug(f"Query combinations: {query_combinations}")
        
        for idx, params in enumerate(query_combinations, 1):
            try:
                logger.debug(f"Executing query {idx}/{len(query_combinations)} with params: {params}")
                result = news_api.get_top_headlines(**params)
                articles = result.get('articles', [])
                logger.debug(f"Query {idx} returned {len(articles)} articles")
                all_articles.extend(articles)
            except Exception as e:
                logger.warning(f"Error fetching articles for query {idx} (params: {params}): {str(e)}")
                continue
        
        logger.info(f"Total articles collected before deduplication: {len(all_articles)}")
        
        # Remove duplicates based on URL
        unique_articles = {article['url']: article for article in all_articles}
        final_count = len(unique_articles)
        
        logger.info(f"After deduplication: {final_count} unique articles")
        logger.info(f"Removed {len(all_articles) - final_count} duplicate articles")
        
        return {
            'articles': list(unique_articles.values()),
            'totalResults': final_count
        }
    except Exception as e:
        logger.error(f"Unexpected error in fetch_top_headlines: {str(e)}", exc_info=True)
        return {'articles': [], 'totalResults': 0}