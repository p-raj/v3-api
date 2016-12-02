# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-02 11:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('terminals', '0003_auto_20161129_1145'),
    ]

    operations = [
        migrations.AddField(
            model_name='terminal',
            name='name',
            field=models.CharField(default=None, max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='terminal',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
