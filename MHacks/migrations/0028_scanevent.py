# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-09-17 00:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MHacks', '0027_delete_pushtoken'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScanEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=60, unique=True)),
                ('number_of_allowable_scans', models.IntegerField(default=1)),
                ('expiry_date', models.DateField(blank=True)),
                ('users', models.ManyToManyField(related_name='scan_event_users', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
