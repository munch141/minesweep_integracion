# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-20 01:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accordion', '0004_auto_20171020_0117'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accordion',
            name='panels',
        ),
        migrations.AddField(
            model_name='accordion',
            name='panel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='panels', to='accordion.Accordion'),
        ),
    ]
