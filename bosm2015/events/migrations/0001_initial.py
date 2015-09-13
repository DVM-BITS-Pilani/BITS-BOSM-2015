# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EventNew',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('content', ckeditor.fields.RichTextField()),
                ('description', models.CharField(max_length=140, blank=True)),
                ('icon', models.ImageField(upload_to=b'icons', blank=True)),
                ('date', models.CharField(default=b'TBA', max_length=100)),
                ('time', models.CharField(default=b'TBA', max_length=100)),
                ('venue', models.CharField(default=b'TBA', max_length=100)),
                ('endtime', models.CharField(default=b'TBA', max_length=100)),
            ],
            options={
                'verbose_name_plural': 'events',
            },
        ),
    ]
