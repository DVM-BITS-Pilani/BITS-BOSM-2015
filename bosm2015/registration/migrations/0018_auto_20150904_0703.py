# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0017_participant_bill_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='bill_id',
            field=models.BigIntegerField(null=True, blank=True),
        ),
    ]
