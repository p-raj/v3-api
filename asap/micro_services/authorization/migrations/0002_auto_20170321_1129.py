# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-21 11:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='authorization',
            unique_together=set([('source', 'target')]),
        ),
    ]
