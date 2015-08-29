# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0002_auto_20150829_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='id',
            field=models.BigIntegerField(serialize=False, primary_key=True),
        ),
    ]
