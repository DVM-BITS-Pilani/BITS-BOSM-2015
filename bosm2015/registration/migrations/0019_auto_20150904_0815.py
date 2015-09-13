# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0018_auto_20150904_0703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='bill_id',
            field=models.BigIntegerField(default=None, null=True),
        ),
    ]
