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
    from .services import save_newsapi_to_db

    logger.info("Starting fetch_latest_news_task...")
    save_newsapi_to_db()
    logger.info("Completed fetch_latest_news_task.")