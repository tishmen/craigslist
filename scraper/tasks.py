import logging
import traceback

from celery import shared_task

from scraper.craigslist import CraigslistScraper
from scraper.email import EmailSender
from scraper.models import ScraperResult, SenderResult

log = logging.getLogger('craigslist')


@shared_task(bind=True)
def scrape_task(self, scraper_obj):
    try:
        scraper = CraigslistScraper()
        results = scraper.scrape(
            scraper_obj.name,
            scraper_obj.account.email,
            scraper_obj.account.password,
            scraper_obj.min_price,
            scraper_obj.max_price,
            scraper_obj.bedroom_count,
            scraper_obj.posting_count,
        )
        for r in results:
            result, _ = ScraperResult.objects.get_or_create(**r)
    except Exception:
        log.error('Traceback: {}'.format(traceback.format_exc()))
        raise


@shared_task(bind=True)
def send_task(self, sender_obj):
    try:
        sender = EmailSender()
        results = sender.send(
            sender_obj.name,
            sender_obj.email.email,
            sender_obj.email.password,
            sender_obj.recipients,
            sender_obj.subject,
            sender_obj.body
        )
        for r in results:
            result, _ = SenderResult.objects.get_or_create(**r)
    except Exception:
        log.error('Traceback: {}'.format(traceback.format_exc()))
        raise
