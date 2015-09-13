# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0004_auto_20150811_1243'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='default_limits',
            field=models.BooleanField(default=True),
        ),
    ]
