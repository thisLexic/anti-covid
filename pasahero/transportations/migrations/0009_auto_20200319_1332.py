# Generated by Django 2.2.5 on 2020-03-19 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transportations', '0008_times_capacity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='times',
            name='capacity',
            field=models.IntegerField(),
        ),
    ]
