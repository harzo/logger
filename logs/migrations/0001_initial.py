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
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('summary', models.TextField()),
                ('problems', models.TextField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('gap_time', models.IntegerField()),
                ('closed', models.BooleanField(default=False)),
                ('id_user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
