# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snippet',
            name='title',
            field=models.CharField(default=b'', max_length=100, blank=True),
        ),
    ]
