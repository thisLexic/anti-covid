# Generated by Django 2.2.5 on 2020-03-20 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commuters', '0003_auto_20200320_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='commuters',
            name='comments',
            field=models.CharField(default='', max_length=512),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='commuters',
            name='preferred_pick_up',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
    ]
