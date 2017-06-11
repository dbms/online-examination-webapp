# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-11 08:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlinetest', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='clientsTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orgname', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=120, unique=True)),
                ('orgSize', models.CharField(max_length=20)),
                ('orgType', models.CharField(max_length=100)),
                ('contactNumber', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=200)),
                ('pwd', models.CharField(max_length=80)),
            ],
        ),
        migrations.DeleteModel(
            name='Users',
        ),
    ]