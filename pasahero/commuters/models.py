import datetime
from django.db import models
from django.contrib.auth.models import User
from cities.models import Cities, Provinces
from transportations.models import Routes
from employees.models import Employees

class Commuters(models.Model):
    lives_city_id = models.ForeignKey(Cities, related_name='commuters', on_delete=models.PROTECT)
    works_city_id = models.ForeignKey(Cities, related_name='workers', on_delete=models.PROTECT)
    lives_province_id = models.ForeignKey(Provinces, related_name='commuters', on_delete=models.PROTECT)
    works_province_id = models.ForeignKey(Provinces, related_name='workers', on_delete=models.PROTECT)
    user_id = models.OneToOneField(User, related_name='commuter', on_delete=models.PROTECT, blank=True, null=True)
    preferred_pick_up = models.CharField(max_length=128, blank=True, null=True)
    last_name = models.CharField(max_length=64)
    first_name = models.CharField(max_length=64)
    middle_name = models.CharField(max_length=64, blank=True, null=True)
    profession = models.CharField(max_length=64)
    company_name = models.CharField(max_length=64)
    company_location = models.CharField(max_length=256)
    present_address = models.CharField(max_length=256)
    permanent_address = models.CharField(max_length=256)
    cell_number = models.CharField(max_length=32, blank=True, null=True)
    tele_number = models.CharField(max_length=32, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    comments = models.CharField(max_length=512, blank=True, null=True)

    def __str__(self):
        return self.last_name + ", " + self.first_name

class Allowed_Routes(models.Model):
    class Meta:
        unique_together = ['route_id', 'commuter_id']
    route_id = models.ForeignKey(Routes, related_name='allowed_routes', on_delete=models.CASCADE)
    commuter_id = models.ForeignKey(Commuters, related_name='allowed_routes', on_delete=models.CASCADE)
    employee_id = models.ForeignKey(Employees, related_name="allowed_routes", on_delete=models.SET_NULL, blank=True, null=True)
    requested_at = models.DateField(default=datetime.datetime.now)

    STATUS_CHOICES = (
            ('A','Allowed'),
            ('P', 'Pending'),
            ('R','Rejected'),
        )
    status = models.CharField(max_length=512, choices=STATUS_CHOICES, default='P')

    def __str__(self):
        return str(self.commuter_id) + " " + str(self.route_id)