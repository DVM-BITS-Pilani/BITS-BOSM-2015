# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0011_auto_20150823_1634'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='barcode',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
