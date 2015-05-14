# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BajarCaja', '0004_file_scale_sz'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='size',
            field=models.FloatField(default=0.0),
        ),
    ]
