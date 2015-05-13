# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BajarCaja', '0002_auto_20150510_0159'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='public',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
