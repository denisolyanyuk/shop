# Generated by Django 3.0.7 on 2020-07-01 14:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20200701_1642'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Item',
            new_name='Product',
        ),
        migrations.RenameModel(
            old_name='ItemImages',
            new_name='ProductImages',
        ),
    ]