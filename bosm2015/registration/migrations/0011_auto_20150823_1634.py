# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0010_auto_20150822_0501'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='confirm',
            name='event',
        ),
        migrations.RemoveField(
            model_name='confirm',
            name='participant',
        ),
        migrations.AlterField(
            model_name='participant',
            name='events',
            field=models.ManyToManyField(to='events.EventNew', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='eventlimits',
            unique_together=set([]),
        ),
        migrations.DeleteModel(
            name='Confirm',
        ),
    ]
