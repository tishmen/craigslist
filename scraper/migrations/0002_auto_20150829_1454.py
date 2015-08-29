# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scraper',
            name='posting_count',
        ),
        migrations.AddField(
            model_name='scraper',
            name='max_postings',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='scraper',
            name='min_postings',
            field=models.IntegerField(default=1),
        ),
    ]
