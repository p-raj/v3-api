# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-02 13:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('runtime', '0006_auto_20170602_1023'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='state',
            field=models.CharField(choices=[('started', 'Started'), ('paused', 'Paused'), ('resumed', 'Resumed'), ('success', 'Success'), ('cancelled', 'Cancelled'), ('killed', 'Killed'), ('expired', 'Expired')], default='started', max_length=16),
        ),
        migrations.RemoveField(
            model_name='session',
            name='expires_at',
        )
    ]
