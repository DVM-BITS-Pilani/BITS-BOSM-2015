# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0006_auto_20150818_1455'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventlimits',
            options={'verbose_name_plural': 'Event Limits'},
        ),
    ]
