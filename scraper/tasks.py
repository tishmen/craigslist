import logging
import traceback

from celery import shared_task

from scraper.craigslist import CraigslistScraper
from scraper.models import Result

log = logging.getLogger('craigslist')


@shared_task(bind=True)
def scrape_task(self, obj):
    try:
        scraper = CraigslistScraper()
        results = scraper.scrape(obj)
        for result in results:
            res, _ = Result.objects.get_or_create(**result)
    except Exception:
        log.error('Traceback: {}'.format(traceback.format_exc()))
        raise
