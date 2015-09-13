# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_eventnew_max_limit'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventnew',
            name='min_limit',
            field=models.IntegerField(default=2),
        ),
    ]
