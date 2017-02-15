# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-15 07:50
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('widgets', '0006_widget_template'),
    ]

    operations = [
        migrations.AddField(
            model_name='widget',
            name='data',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='Widget Data, the data to be filled by admin, using admin widget designed by developer', null=True, verbose_name='Widget Data'),
        ),
    ]
