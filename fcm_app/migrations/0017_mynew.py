# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-15 12:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fcm_app', '0016_auto_20171115_1345'),
    ]

    operations = [
        migrations.CreateModel(
            name='mynew',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=2000)),
            ],
        ),
    ]