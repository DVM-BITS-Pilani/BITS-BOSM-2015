# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0019_auto_20150904_0815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='bill_id',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
