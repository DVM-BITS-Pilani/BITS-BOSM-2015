# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0005_userprofile_default_limits'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='email_id',
            field=models.EmailField(max_length=254, blank=True),
        ),
    ]
