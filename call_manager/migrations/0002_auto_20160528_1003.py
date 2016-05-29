# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-28 10:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('call_manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicallogentry',
            name='survival_status',
            field=models.CharField(choices=[('alive', 'Alive'), ('dead', 'Dead'), ('unknown', 'Unknown')], max_length=10, null=True, verbose_name='Survival status of the participant'),
        ),
        migrations.AlterField(
            model_name='logentry',
            name='survival_status',
            field=models.CharField(choices=[('alive', 'Alive'), ('dead', 'Dead'), ('unknown', 'Unknown')], max_length=10, null=True, verbose_name='Survival status of the participant'),
        ),
    ]