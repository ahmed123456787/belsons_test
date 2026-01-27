from celery import shared_task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@shared_task
def fetch_sources_task():
    from .services import save_api_res_to_db

    logger.info("Starting fetch_sources_task...")
    save_api_res_to_db()
    logger.info("Completed fetch_sources_task.")



@shared_task
def fetch_news_task():
    from .services import fetch_latest_news

    logger.info("Starting fetch_news_task...")
    fetch_latest_news()
    logger.info("Completed fetch_news_task.")