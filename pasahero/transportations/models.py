from django.db import models
from cities.models import Cities, Provinces
from employees.models import Employees

class Routes(models.Model):
    city_id = models.ForeignKey(Cities, related_name="routes", on_delete=models.CASCADE)
    province_id = models.ForeignKey(Provinces, related_name="routes", on_delete=models.CASCADE)
    employee_id = models.ForeignKey(Employees, related_name="routes", on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=256)
    via = models.CharField(max_length=256)
    is_active = models.BooleanField(default=True)
    point_a = models.CharField(max_length=256)
    point_b = models.CharField(max_length=256)

    def __str__(self):
        return str(self.name)

class Directions(models.Model):
    route_id = models.ForeignKey(Routes, related_name="directions", on_delete=models.CASCADE)
    start_location = models.CharField(max_length=128)
    end_location = models.CharField(max_length=128)
    vehicle = models.CharField(max_length=64)
    duration_minutes = models.IntegerField()

    def __str__(self):
        return str(self.start_location) + " " + str(self.end_location)

    def ordered_times(self):
        return self.times.order_by('time')

class Times(models.Model):
    class Meta:
        unique_together = ['direction_id', 'time']
    direction_id = models.ForeignKey(Directions, related_name='times', on_delete=models.CASCADE)
    time = models.TimeField()
    capacity = models.IntegerField()

    def __str__(self):
        return str(self.time)

    def str_time(self):
        return self.time.strftime("%-I:%M:%p")