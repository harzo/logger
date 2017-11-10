# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0002_auto_20150415_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='gap_time',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='log',
            name='problems',
            field=models.TextField(blank=True, null=True),
        ),
    ]
