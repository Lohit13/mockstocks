# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0008_auto_20160810_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corelate',
            name='company',
            field=models.ForeignKey(to='game.Company'),
        ),
        migrations.AlterField(
            model_name='corelate',
            name='shares',
            field=models.IntegerField(),
        ),
    ]
