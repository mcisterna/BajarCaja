# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BajarCaja', '0005_auto_20150513_2355'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='real_size',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
