# Generated by Django 2.2.5 on 2020-03-19 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transportations', '0003_times'),
    ]

    operations = [
        migrations.AddField(
            model_name='transportations',
            name='road',
            field=models.CharField(default='df', max_length=128),
        ),
    ]