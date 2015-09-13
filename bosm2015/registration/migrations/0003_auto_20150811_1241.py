# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_auto_20150731_2332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='coach',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='participant',
            name='gender',
            field=models.CharField(max_length=10, choices=[(b'M', b'Male'), (b'F', b'Female')]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='firstname',
            field=models.CharField(max_length=200, verbose_name=b'First Name'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='lastname',
            field=models.CharField(max_length=200, verbose_name=b'Last Name'),
        ),
    ]
