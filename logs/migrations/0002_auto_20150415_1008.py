# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='gap_time',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='log',
            name='problems',
            field=models.TextField(null=True),
        ),
    ]
