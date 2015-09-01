from django.contrib import admin, messages

from scraper.models import (
    Account, Email, Scraper, Sender, ScraperResult, SenderResult
)
from scraper.tasks import scrape_task, send_task


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):

    pass


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):

    pass


@admin.register(Scraper)
class ScraperAdmin(admin.ModelAdmin):

    list_display = ('name', 'account')
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


@admin.register(Sender)
class SenderAdmin(admin.ModelAdmin):

    list_display = ('name', 'email')
    actions = ('send', )

    def send(self, request, queryset):
        count = queryset.count()
        for result in queryset:
            send_task.delay(result)
        if count == 1:
            message_bit = '1 sender'
        else:
            message_bit = '{} senders'.format(count)
        self.message_user(
            request,
            'Delayed send_task for {}'.format(message_bit),
            level=messages.SUCCESS
        )

    send.short_description = 'Run selected senders'


@admin.register(ScraperResult)
class ScraperResultAdmin(admin.ModelAdmin):

    pass


@admin.register(SenderResult)
class SenderResultAdmin(admin.ModelAdmin):

    pass
