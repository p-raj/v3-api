# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-28 13:03
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bouncer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='meta',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}),
        ),
    ]
