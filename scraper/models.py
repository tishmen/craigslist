from django.db import models


class Account(models.Model):

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.email


class Email(models.Model):

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.email


class Scraper(models.Model):

    name = models.CharField(max_length=100, unique=True)
    account = models.ForeignKey('Account')
    posting_count = models.IntegerField(default=1)
    min_price = models.IntegerField(default=0)
    max_price = models.IntegerField(default=2000)
    bedroom_count = models.IntegerField(default=2)

    def __str__(self):
        return self.name


class Sender(models.Model):

    name = models.CharField(max_length=100, unique=True)
    email = models.ForeignKey('Email')
    recipients = models.ManyToManyField('ScraperResult')
    subject = models.TextField()
    body = models.TextField()

    def __str__(self):
        return self.name


class ScraperResult(models.Model):

    class Meta:

        unique_together = ('url', 'email')

    email = models.EmailField()
    url = models.URLField()

    def __str__(self):
        return self.email


class SenderResult(models.Model):

    sender = models.CharField(max_length=100)
    recipient = models.CharField(max_length=100)
    subject = models.TextField()
    body = models.TextField()

    def __str__(self):
        return self.message
