# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventLimits',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('limit', models.IntegerField()),
                ('event', models.ForeignKey(to='events.EventNew')),
            ],
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name_plural': 'User Profiles'},
        ),
        migrations.AddField(
            model_name='userprofile',
            name='state',
            field=models.CharField(default='NA', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='participant',
            name='acco',
            field=models.NullBooleanField(verbose_name=b'passed recnacc'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='controlzpay',
            field=models.NullBooleanField(verbose_name=b'passed controlz'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='firewallz',
            field=models.NullBooleanField(verbose_name=b'passed firewallz'),
        ),
        migrations.AddField(
            model_name='eventlimits',
            name='leader',
            field=models.ForeignKey(to='registration.UserProfile'),
        ),
    ]
