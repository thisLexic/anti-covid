from django.db import models
from django.contrib.auth.models import User

class Provinces(models.Model):
    name = models.CharField(max_length=256, unique=True)
    def __str__(self):
        return self.name

class Cities(models.Model):
    class Meta:
        unique_together=['name', 'province_id']
    user_id = models.OneToOneField(User, related_name='city', on_delete=models.PROTECT)
    province_id = models.ForeignKey(Provinces,related_name='cities', on_delete=models.PROTECT)
    name = models.CharField(max_length=256)
    major_announcement = models.TextField(blank=True, null=True)
    major_is_active = models.BooleanField(default=True)
    minor_announcement = models.TextField(blank=True, null=True)
    minor_is_active = models.BooleanField(default=True)
    cell_number = models.CharField(max_length=32)
    tele_number = models.CharField(max_length=32, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name