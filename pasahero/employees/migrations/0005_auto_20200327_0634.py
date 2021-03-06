# Generated by Django 2.2.5 on 2020-03-27 06:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0004_employees_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employees',
            name='city_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='employees', to='cities.Cities'),
        ),
        migrations.AlterField(
            model_name='employees',
            name='user_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='employee', to=settings.AUTH_USER_MODEL),
        ),
    ]
