# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-16 07:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_resourceschema'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resourceschema',
            name='resource',
        ),
        migrations.DeleteModel(
            name='ResourceSchema',
        ),
    ]
