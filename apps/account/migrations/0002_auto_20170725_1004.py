# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-25 10:04
from __future__ import unicode_literals

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='created',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True,
                                       verbose_name='Created'),
        ),
        migrations.AddField(
            model_name='account',
            name='last_updated',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True,
                                       verbose_name='Last Updated'),
        ),
        migrations.AlterField(
            model_name='account',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
    ]
