# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0003_auto_20150415_1010'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='date_add',
            field=models.DateTimeField(null=True, auto_now_add=True),
        ),
        migrations.AddField(
            model_name='log',
            name='date_mod',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
