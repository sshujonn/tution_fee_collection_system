# Generated by Django 3.2 on 2021-04-14 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='fee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee_name', models.CharField(max_length=50)),
                ('fee_amount', models.CharField(max_length=10)),
            ],
        ),
    ]