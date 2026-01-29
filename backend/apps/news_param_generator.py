from .news.models import Country, Category
import random


def sample_filters(countries_count=None, categories_count=None):
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
    
    
    return sampled_countries, sampled_categories


def build_query_combinations(countries=None, categories=None, sources=None):
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
    
    return combinations
