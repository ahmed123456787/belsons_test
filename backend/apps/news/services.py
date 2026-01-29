from ..fetch_news import fetch_sources, fetch_top_headlines
from .models import Source, Category, Language, Country, NewsArticle
from django.db import transaction
from datetime import datetime

    
def save_sources_to_db() -> None:
    """
    Fetches news sources from an external API and saves them to the database.
    """
    try:
        with transaction.atomic():
            sources = fetch_sources()
            if not sources:
                return
            
            # delete all the existing sources
            Source.objects.all().delete()

            for source in sources:
                source_id = source.get('id')
                if not source_id:
                    continue
                
                source = Source.objects.create(
                    source_id=source_id, 
                    name=source.get('name', ''),
                    description=source.get('description', ''),
                    url=source.get('url', ''),
                    category=Category.objects.filter(name=source.get('category')).first(),
                    language=Language.objects.filter(code=source.get('language')).first(),
                    country=Country.objects.filter(code=source.get('country')).first(),
                )
                source.save()   
            
    except Exception as e:
        print(f"Error saving sources: {e}")
        return


def save_top_headlines_to_db(countries=None, categories=None, sources=None, sample_countries=None, sample_categories=None):
    """
    Fetches top headlines from NewsAPI and saves them to the database.
    
    Args:
        countries (list): Specific country codes (e.g., ['us', 'fr'])
        categories (list): Specific category names (e.g., ['business', 'technology'])
        sources (list): Specific source IDs (e.g., ['bbc-news'])
        sample_countries (int): Randomly sample N countries (e.g., 4)
        sample_categories (int): Randomly sample N categories (e.g., 20)
    """
    try:
        # Fetch headlines using the specified filters
        result = fetch_top_headlines(
            countries=countries,
            categories=categories,
            sources=sources,
            sample_countries=sample_countries,
            sample_categories=sample_categories
        )
        
        articles = result.get('articles', [])
        
        if not articles:
            print("No articles fetched from NewsAPI")
            return
        
        created_count = 0
        updated_count = 0
        
        with transaction.atomic():
            for article_data in articles:
                try:
                    # Skip articles without required fields
                    if not article_data.get('url') or not article_data.get('title'):
                        continue
                    
                    # Try to get the source
                    source = None
                    source_name = article_data.get('source', {}).get('name')
                    if source_name:
                        source = Source.objects.filter(name=source_name).first()
                    
                    # Parse published date
                    published_at = article_data.get('publishedAt')
                    if published_at and isinstance(published_at, str):
                        try:
                            published_at = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                        except:
                            continue
                    else:
                        continue
                    
                    # Create or update the article
                    article, created = NewsArticle.objects.get_or_create(
                        url=article_data.get('url'),
                        defaults={
                            'title': article_data.get('title', ''),
                            'description': article_data.get('description', ''),
                            'content': article_data.get('content', ''),
                            'image_url': article_data.get('urlToImage', ''),
                            'published_at': published_at,
                            'source': source,
                        }
                    )
                    
                    if created:
                        # Auto-populate denormalized fields from source
                        if source:
                            article.category = source.category
                            article.language = source.language
                            article.country = source.country
                            article.save()
                        created_count += 1
                    else:
                        updated_count += 1
                
                except Exception as e:
                    print(f"Error saving article: {e}")
                    continue
        
        print(f"Successfully saved articles - Created: {created_count}, Updated: {updated_count}")
        
    except Exception as e:
        print(f"Error in save_top_headlines_to_db: {e}")
        return