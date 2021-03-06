# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-11 14:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client', '0001_initial'),
        ('task', '0001_initial'),
        ('project', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='Description')),
                ('starttime', models.DateTimeField(blank=True, null=True, verbose_name='Start date / time')),
                ('endtime', models.DateTimeField(blank=True, null=True, verbose_name='End date / time')),
                ('duration', models.IntegerField(blank=True, null=True, verbose_name='Duration')),
                ('comments', models.TextField(blank=True, null=True, verbose_name='Comments')),
                ('cost', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=8, null=True, verbose_name='Cost')),
                ('created', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Created')),
                ('last_updated', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Last Updated')),
                ('client', models.ForeignKey(blank=True, db_column='Client', null=True, on_delete=django.db.models.deletion.SET_NULL, to='client.Client')),
                ('project', models.ForeignKey(blank=True, db_column='Project', null=True, on_delete=django.db.models.deletion.SET_NULL, to='project.Project')),
                ('task', models.ForeignKey(blank=True, db_column='Task', null=True, on_delete=django.db.models.deletion.SET_NULL, to='task.Task')),
                ('user', models.ForeignKey(blank=True, db_column='User', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Entry',
                'verbose_name_plural': 'Entries',
            },
        ),
    ]
