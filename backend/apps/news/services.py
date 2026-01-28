from ..fetch_news import fetch_sources, fetch_latest_news
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
        

def save_newsapi_to_db():
    """
    Fetches news articles from NewsAPI and saves them to the database.
    """
    try:
        result = fetch_latest_news()
        articles = result.get('articles', [])
        
        if not articles:
            print("No articles fetched from NewsAPI")
            return
        
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
                
                except Exception as e:
                    print(f"Error saving article: {e}")
                    continue
        
        print(f"Successfully saved {len(articles)} articles")
    except Exception as e:
        print(f"Error in save_newsapi_to_db: {e}")
        return