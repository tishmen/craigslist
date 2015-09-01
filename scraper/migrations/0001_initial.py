# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Scraper',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('posting_count', models.IntegerField(default=1)),
                ('min_price', models.IntegerField(default=0)),
                ('max_price', models.IntegerField(default=2000)),
                ('bedroom_count', models.IntegerField(default=2)),
                ('account', models.ForeignKey(to='scraper.Account')),
            ],
        ),
        migrations.CreateModel(
            name='ScraperResult',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('url', models.URLField(unique=True)),
                ('email', models.EmailField(unique=True, max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Sender',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('subject', models.TextField()),
                ('body', models.TextField()),
                ('email', models.ForeignKey(to='scraper.Email')),
                ('recipients', models.ManyToManyField(to='scraper.ScraperResult')),
            ],
        ),
        migrations.CreateModel(
            name='SenderResult',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('message', models.TextField(unique=True)),
            ],
        ),
    ]
