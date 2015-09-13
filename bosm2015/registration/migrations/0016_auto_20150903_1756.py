# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0015_participant_sport_leader'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='fid',
            field=models.NullBooleanField(verbose_name=b'passed inner booth'),
        ),
    ]
