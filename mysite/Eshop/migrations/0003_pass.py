# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Eshop', '0002_auto_20181225_1447'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Dual', models.CharField(default=b'', max_length=255)),
            ],
        ),
    ]
