# Generated by Django 5.1.1 on 2024-09-06 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomrate',
            name='room_id',
            field=models.IntegerField(unique=True),
        ),
    ]
