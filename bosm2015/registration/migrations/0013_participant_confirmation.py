# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0012_participant_barcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='confirmation',
            field=models.BooleanField(default=False),
        ),
    ]
