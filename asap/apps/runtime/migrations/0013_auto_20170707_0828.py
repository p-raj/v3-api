# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-07 08:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('runtime', '0012_auto_20170621_0547'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='runtime',
            name='widget_locker_token',
        ),
        migrations.RemoveField(
            model_name='runtime',
            name='widget_locker_uuid',
        ),
    ]
