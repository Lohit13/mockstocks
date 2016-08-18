# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0013_auto_20160818_2108'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='nextclose',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
