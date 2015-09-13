# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0013_participant_confirmation'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='barcode',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
