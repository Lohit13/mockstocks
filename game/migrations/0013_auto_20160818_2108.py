# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0012_auto_20160818_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='nextvol',
            field=models.BigIntegerField(default=0),
        ),
    ]
