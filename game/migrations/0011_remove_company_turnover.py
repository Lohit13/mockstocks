# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0010_auto_20160810_1057'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='turnover',
        ),
    ]
