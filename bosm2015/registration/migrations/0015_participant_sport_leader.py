# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0014_userprofile_barcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='sport_leader',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
