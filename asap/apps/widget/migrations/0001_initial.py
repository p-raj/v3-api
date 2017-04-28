# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-28 09:55
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Widget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('processes_json', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('process_locker_uuid', models.CharField(max_length=512)),
                ('process_locker_token', models.CharField(help_text='Token of Process Locker to which will be loaded when a Widget is called.', max_length=512, verbose_name='Process Locker Token')),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='Widget Data, the data to be filled by admin, using admin widget designed by developer', null=True, verbose_name='Widget Data')),
                ('rules', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='Widget Rules')),
                ('workflow_uuid', models.CharField(blank=True, max_length=512, null=True)),
                ('template', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='Widget Template, the list of components with their layout & styles', null=True, verbose_name='Widget Template')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_widget_widget', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WidgetLocker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('rules', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='Rules config, tells us which widget will be called based on what rules.', null=True, verbose_name='Widget rules')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_widget_widgetlocker', to=settings.AUTH_USER_MODEL)),
                ('widgets', models.ManyToManyField(to='widget.Widget')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
