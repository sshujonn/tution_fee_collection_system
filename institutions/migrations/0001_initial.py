# Generated by Django 3.1.2 on 2021-04-10 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StudentClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institution_name', models.CharField(max_length=150)),
                ('institution_address', models.CharField(max_length=200)),
                ('institution_phone_number', models.CharField(max_length=30)),
            ],
        ),
    ]
