# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
        ('regsoft', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('gender', models.CharField(max_length=10)),
                ('phone', models.BigIntegerField()),
                ('email_id', models.EmailField(max_length=254)),
                ('firewallz', models.NullBooleanField()),
                ('fid', models.IntegerField(null=True, blank=True)),
                ('acco', models.NullBooleanField()),
                ('controlzpay', models.NullBooleanField()),
                ('fireid', models.CharField(max_length=100, null=True, blank=True)),
                ('coach', models.NullBooleanField()),
                ('events', models.ManyToManyField(to='events.EventNew', blank=True)),
                ('gleader', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('room', models.ForeignKey(blank=True, to='regsoft.Room', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstname', models.CharField(max_length=200)),
                ('lastname', models.CharField(max_length=200)),
                ('college', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('phone', models.BigIntegerField(blank=True)),
                ('email_id', models.EmailField(max_length=254, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
    ]
