# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-20 12:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0004_auto_20170720_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ttask',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=4, null=True, verbose_name='Price'),
        ),
    ]
