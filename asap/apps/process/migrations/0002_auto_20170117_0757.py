# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-17 07:57
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcessLogs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logId', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Non-editable, to be generated by system itself. To be returned in response, logs can be             fetched using this important in case do not want to share your primary key', unique=True, verbose_name='Log unique id')),
                ('started_at', models.DateTimeField(db_index=True, help_text='When process initiated its task.', verbose_name='Process execution start time.')),
                ('ended_at', models.DateTimeField(db_index=True, help_text='When process completed its task.', verbose_name='Process execution end time.')),
                ('dataIn', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='Process request payload, includes query_params, data etc.', null=True, verbose_name='Process Request payload')),
                ('dataOut', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='Response that is rerturned via Process.', null=True, verbose_name='Process Request response')),
                ('status', models.CharField(choices=[('init', 'Initialize'), ('inprocess', 'In Process'), ('wait', 'Waiting'), ('succeeded', 'Completed'), ('failed', 'Failed')], default='init', help_text='Process Request state at any given time.', max_length=20, verbose_name='current state of process request')),
                ('process', models.ForeignKey(help_text='Process to which this log belongs too.', on_delete=django.db.models.deletion.CASCADE, related_name='process_logs', to='process.Process', verbose_name='process')),
            ],
            options={
                'verbose_name': 'Process Logs',
                'get_latest_by': 'id',
                'verbose_name_plural': 'Processes Logs',
                'ordering': ['-id'],
            },
        ),
        migrations.AlterField(
            model_name='processlocker',
            name='token',
            field=models.UUIDField(blank=True, editable=False, help_text='Non-editable, to be generated by system itself and only when is_publish=True ,                    means when Process Locker is Published.', null=True, unique=True, verbose_name='Process token'),
        ),
    ]
