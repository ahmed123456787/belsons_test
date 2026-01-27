from ..fetch_news import fetch_sources, fetch_latest_news
from .models import Source, Category, Language, Country
from django.db import transaction

    
def save_api_res_to_db() -> None:
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
    Fetches news sources from NewsAPI and saves them to the database.
    """
    fetch_latest_news()