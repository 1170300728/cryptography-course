# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Eshop', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sale',
            old_name='Weight',
            new_name='Size',
        ),
    ]
