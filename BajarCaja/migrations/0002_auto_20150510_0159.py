# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BajarCaja', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='file',
            old_name='name',
            new_name='filename',
        ),
    ]
