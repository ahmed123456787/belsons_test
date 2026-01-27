from celery import shared_task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@shared_task
def sample_task():
    logger.info("The sample task just ran.")


@shared_task
def fetch_sources_task():
    from .services import save_api_res_to_sources

    logger.info("Starting fetch_sources_task...")
    save_api_res_to_sources()
    logger.info("Completed fetch_sources_task.")