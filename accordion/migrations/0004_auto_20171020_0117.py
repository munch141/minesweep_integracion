# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-20 01:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accordion', '0003_auto_20171019_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accordion',
            name='height',
            field=models.CharField(blank=True, default='30', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='accordion',
            name='width',
            field=models.CharField(blank=True, default='100', max_length=50, null=True),
        ),
    ]
