# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-11 12:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fcm_app', '0028_auto_20180925_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='fcm',
            name='image_url',
            field=models.TextField(null=True),
        ),
    ]