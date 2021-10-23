import logging

from celery import shared_task

from .models import Campaign

logger = logging.getLogger('django')

@shared_task(bind=True)
def collect_campaigns_metadata(self):
    campaigns = Campaign.collect_metadata()
    logger.info(f"Seccesfully colected metadata for campaigns: {campaigns}")
