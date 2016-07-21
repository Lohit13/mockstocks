# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20160721_1800'),
    ]

    operations = [
        migrations.CreateModel(
            name='Corelate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shares', models.IntegerField(default=0)),
                ('company', models.ForeignKey(to='game.Company')),
                ('user', models.ForeignKey(to='game.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
