# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_offer_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='networth',
        ),
    ]
