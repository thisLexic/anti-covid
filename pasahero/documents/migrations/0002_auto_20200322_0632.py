# Generated by Django 2.2.5 on 2020-03-22 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documents',
            name='document',
            field=models.ImageField(upload_to='commuter_documents/'),
        ),
    ]
