# Generated by Django 3.2 on 2021-04-14 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StudentClass',
            new_name='Institution',
        ),
    ]