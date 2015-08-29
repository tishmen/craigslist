from django.contrib import admin, messages

from scraper.models import Scraper, Result
from scraper.tasks import scrape_task


@admin.register(Scraper)
class ScraperAdmin(admin.ModelAdmin):

    list_display = ('name', 'min_price', 'max_price', 'bedroom_count')
    actions = ('scrape', )

    def scrape(self, request, queryset):
        count = queryset.count()
        for scraper in queryset:
            scrape_task.delay(scraper)
        if count == 1:
            message_bit = '1 scraper'
        else:
            message_bit = '{} scrapers'.format(count)
        self.message_user(
            request,
            'Delayed scrape_task for {}'.format(message_bit),
            level=messages.SUCCESS
        )

    scrape.short_description = 'Run selected scrapers'


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):

    list_display = ('email', 'id', 'added')
