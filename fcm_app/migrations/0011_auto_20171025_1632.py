# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-10-25 13:32
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fcm_app', '0010_fcm_concept_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fcm_concept_info',
            name='info',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
