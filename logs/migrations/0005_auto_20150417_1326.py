# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0004_auto_20150415_1054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='gap_time',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
