# Generated by Django 3.0.7 on 2020-07-31 16:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_auto_20200720_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 31, 19, 43, 20, 2102)),
        ),
    ]