# Generated by Django 3.0.7 on 2020-07-20 12:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_auto_20200720_1501'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitemmodel',
            name='price',
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 20, 15, 5, 44, 646154)),
        ),
    ]
