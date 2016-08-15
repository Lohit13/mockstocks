# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_news'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='initshares',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
