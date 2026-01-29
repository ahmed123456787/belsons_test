from celery import shared_task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@shared_task
def fetch_sources_task():
    from .services import save_sources_to_db

    logger.info("Starting fetch_sources_task...")
    save_sources_to_db()
    logger.info("Completed fetch_sources_task.")



@shared_task
def fetch_latest_news_task():
    from .services import save_top_headlines_to_db

    logger.info("Starting fetch_latest_news_task...")
    # Sample 4 countries and 20 categories
    save_top_headlines_to_db(sample_countries=4, sample_categories=10)

    # # Specific countries and categories
    # save_top_headlines_to_db(countries=['us', 'fr'], categories=['business', 'technology'])

    # # Sample 5 countries with specific categories
    # save_top_headlines_to_db(sample_countries=5, categories=['sports', 'health'])

    # # Specific sources
    # save_top_headlines_to_db(sources=['bbc-news', 'cnn'])
    logger.info("Completed fetch_latest_news_task.")