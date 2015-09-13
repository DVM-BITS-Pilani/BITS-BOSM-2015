# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_eventnew_min_limit'),
        ('registration', '0008_auto_20150820_1502'),
    ]

    operations = [
        migrations.CreateModel(
            name='Confirm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('confirm', models.BooleanField(default=False)),
                ('event', models.ForeignKey(to='events.EventNew')),
                ('participant', models.ForeignKey(to='registration.Participant')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='eventlimits',
            unique_together=set([('event', 'leader')]),
        ),
    ]
