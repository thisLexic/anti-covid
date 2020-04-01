# Generated by Django 2.2.5 on 2020-03-19 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Provinces',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('major_announcement', models.TextField(blank=True)),
                ('minor_announcement', models.TextField(blank=True)),
                ('cell_number', models.CharField(max_length=32)),
                ('tele_number', models.CharField(blank=True, max_length=32)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('province_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='cities.Provinces')),
            ],
            options={
                'unique_together': {('name', 'province_id')},
            },
        ),
    ]
