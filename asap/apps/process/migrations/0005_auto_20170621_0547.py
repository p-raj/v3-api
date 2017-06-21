# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-21 05:47
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0004_remove_process_is_system'),
    ]

    operations = [
        migrations.AlterField(
            model_name='process',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='processlocker',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, max_length=64, unique=True),
        ),
    ]
