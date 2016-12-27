# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Instance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=20)),
                ('net', models.CharField(max_length=20)),
                ('private_ip', models.GenericIPAddressField(verbose_name=b'\xe7\xa7\x81\xe6\x9c\x89ip')),
                ('inside_ip', models.GenericIPAddressField(unique=True, verbose_name=b'\xe5\x86\x85\xe9\x83\xa8ip')),
                ('float_ip', models.GenericIPAddressField(unique=True, null=True, verbose_name=b'\xe6\xb5\xae\xe5\x8a\xa8ip', blank=True)),
                ('status', models.BooleanField(default=0)),
            ],
        ),
    ]
