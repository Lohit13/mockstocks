# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('ticker', models.CharField(max_length=10)),
                ('industry', models.CharField(max_length=20)),
                ('turnover', models.BigIntegerField(default=0)),
                ('profit', models.BigIntegerField(default=0)),
                ('shares', models.IntegerField(default=0)),
                ('bookvalue', models.IntegerField(default=0)),
                ('curprice', models.IntegerField(default=0)),
                ('dayhi', models.IntegerField(default=0)),
                ('daylo', models.IntegerField(default=0)),
                ('close', models.IntegerField(default=0)),
                ('netchange', models.IntegerField(default=0)),
                ('yearhi', models.IntegerField(default=0)),
                ('yearlo', models.IntegerField(default=0)),
                ('peratio', models.IntegerField(default=0)),
                ('volumes', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shares', models.IntegerField()),
                ('price', models.IntegerField()),
                ('offered_at', models.DateTimeField()),
                ('company', models.ForeignKey(to='game.Company')),
                ('user', models.ForeignKey(to='game.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bought_at', models.DateTimeField()),
                ('buyer', models.ForeignKey(to='game.UserProfile')),
                ('offer', models.ForeignKey(to='game.Offer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cash',
            field=models.BigIntegerField(default=10000),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='networth',
            field=models.BigIntegerField(default=10000),
            preserve_default=True,
        ),
    ]
