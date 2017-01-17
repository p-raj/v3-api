# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-17 12:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organizations', '0003_member_runtime_locker_uuid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='user',
        ),
        migrations.AddField(
            model_name='organization',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='author_organizations_organization', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='organization',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='organization',
            name='modified_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
