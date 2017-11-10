# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Gap',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('type', models.IntegerField()),
                ('week_day', models.IntegerField(blank=True, null=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('date_add', models.DateTimeField(null=True, auto_now_add=True)),
                ('date_mod', models.DateTimeField(null=True, auto_now=True)),
                ('id_user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
