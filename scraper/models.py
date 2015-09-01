from django.db import models


###############################################################################
# Resources
###############################################################################

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


###############################################################################
# Action objects
###############################################################################

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


###############################################################################
# Results
###############################################################################

class ScraperResult(models.Model):

    id = models.BigIntegerField(primary_key=True)
    url = models.URLField(unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


class SenderResult(models.Model):

    message = models.TextField(unique=True)

    def __str__(self):
        return self.message
