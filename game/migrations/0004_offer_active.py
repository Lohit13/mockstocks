# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_corelate'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
