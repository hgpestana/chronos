# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-04 09:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('comments', models.TextField(blank=True, null=True, verbose_name='Comments')),
                ('type', models.CharField(blank=True, max_length=255, null=True, verbose_name='Type')),
                ('filetype', models.CharField(blank=True, max_length=255, null=True, verbose_name='File type')),
                ('created', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Created')),
                ('user', models.ForeignKey(blank=True, db_column='User', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Report',
                'verbose_name_plural': 'Reports',
            },
        ),
    ]