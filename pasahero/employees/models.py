from django.db import models
from django.contrib.auth.models import User
from cities.models import Cities

class Employees(models.Model):
    user_id = models.OneToOneField(User, related_name='employee', on_delete=models.PROTECT)
    city_id = models.ForeignKey(Cities, related_name='employees', on_delete=models.PROTECT)
    last_name = models.CharField(max_length=64)
    first_name = models.CharField(max_length=64)
    middle_name = models.CharField(max_length=64, blank=True, null=True)
    job_title = models.CharField(max_length=64)
    department = models.CharField(max_length=64)
    present_address = models.CharField(max_length=256, null=True, blank=True)
    permanent_address = models.CharField(max_length=256, null=True, blank=True)
    cell_number = models.CharField(max_length=32, blank=True, null=True)
    tele_number = models.CharField(max_length=32, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    is_active = models.BooleanField(default=True)