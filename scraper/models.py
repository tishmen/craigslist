from django.db import models


class Scraper(models.Model):

    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    min_postings = models.IntegerField(default=1)
    max_postings = models.IntegerField(default=1)
    min_price = models.IntegerField(default=0)
    max_price = models.IntegerField(default=2000)
    bedroom_count = models.IntegerField(default=2)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Result(models.Model):

    id = models.BigIntegerField(primary_key=True)
    email = models.EmailField(unique=True)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
