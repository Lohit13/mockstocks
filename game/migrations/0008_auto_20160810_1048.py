# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0007_company_initshares'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corelate',
            name='company',
            field=models.ForeignKey(blank=True, to='game.Company', null=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='user',
            field=models.ForeignKey(blank=True, to='game.UserProfile', null=True),
        ),
    ]
