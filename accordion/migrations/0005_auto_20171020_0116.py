# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-20 01:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accordion', '0004_auto_20171020_0100'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accordion',
            old_name='acordion_id',
            new_name='accordion_id',
        ),
    ]