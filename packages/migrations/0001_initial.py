# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-10-06 13:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('loginSystem', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('packageName', models.CharField(max_length=50, unique=True)),
                ('diskSpace', models.IntegerField()),
                ('bandwidth', models.IntegerField()),
                ('emailAccounts', models.IntegerField(null=True)),
                ('dataBases', models.IntegerField(default=0)),
                ('ftpAccounts', models.IntegerField(default=0)),
                ('allowedDomains', models.IntegerField(default=0)),
                ('allowFullDomain', models.IntegerField(default=1)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loginSystem.Administrator')),
            ],
        ),
    ]
