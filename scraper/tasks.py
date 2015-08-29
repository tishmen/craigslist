import traceback

from celery import shared_task

from scraper.craigslist import CraigslistScraper
from scraper.models import Result


@shared_task(bind=True)
def scrape_task(self, obj):
    try:
        scraper = CraigslistScraper()
        results = scraper.scrape(obj)
        for result in results:
            res = Result(**result)
            res.save()
    except Exception:
        print('Traceback: %s', traceback.format_exc())
        raise
