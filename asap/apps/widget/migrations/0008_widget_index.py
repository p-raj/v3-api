# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-10 12:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('widget', '0007_auto_20170602_1023'),
    ]

    operations = [
        migrations.AddField(
            model_name='widget',
            name='index',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
