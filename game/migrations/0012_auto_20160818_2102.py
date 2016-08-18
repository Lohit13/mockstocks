# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0011_remove_company_turnover'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='nextvol',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='cash',
            field=models.BigIntegerField(default=100000),
        ),
    ]
