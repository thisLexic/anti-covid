# Generated by Django 2.2.5 on 2020-03-26 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0003_auto_20200322_1813'),
    ]

    operations = [
        migrations.AddField(
            model_name='employees',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
