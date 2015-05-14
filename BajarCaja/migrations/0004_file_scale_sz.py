# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BajarCaja', '0003_file_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='scale_sz',
            field=models.CharField(default=b'B', max_length=2),
            preserve_default=True,
        ),
    ]
