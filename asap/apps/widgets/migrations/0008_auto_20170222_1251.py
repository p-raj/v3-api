# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-22 12:51
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('widgets', '0007_widget_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='widgetlocker',
            name='token',
            field=models.UUIDField(default=uuid.uuid4, editable=False, help_text='Non-editable, to be generated by system itself and only when is_publish=True ,                    means when Widget Locker is Published.', unique=True, verbose_name='Locker token'),
        ),
    ]
