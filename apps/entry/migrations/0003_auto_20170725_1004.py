# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-25 10:04
from __future__ import unicode_literals

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('entry', '0002_auto_20170724_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='created',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True,
                                       verbose_name='Created'),
        ),
        migrations.AddField(
            model_name='entry',
            name='last_updated',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True,
                                       verbose_name='Last Updated'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='duration',
            field=models.IntegerField(blank=True, null=True, verbose_name='Duration'),
        ),
    ]