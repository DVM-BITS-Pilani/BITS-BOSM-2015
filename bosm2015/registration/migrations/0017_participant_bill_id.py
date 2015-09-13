# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0016_auto_20150903_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='bill_id',
            field=models.BigIntegerField(null=True),
        ),
    ]
