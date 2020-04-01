from django.db import models
from commuters.models import Allowed_Routes

class Preferred_Times(models.Model):
    allowed_route_id = models.OneToOneField(Allowed_Routes, related_name='preferred_time', on_delete=models.CASCADE)
    mon_a_to_b = models.TimeField(null=True, blank=True)
    tues_a_to_b = models.TimeField(null=True, blank=True)
    wed_a_to_b = models.TimeField(null=True, blank=True)
    thurs_a_to_b = models.TimeField(null=True, blank=True)
    fri_a_to_b = models.TimeField(null=True, blank=True)
    sat_a_to_b = models.TimeField(null=True, blank=True)
    sun_a_to_b = models.TimeField(null=True, blank=True)
    mon_b_to_a = models.TimeField(null=True, blank=True)
    tues_b_to_a = models.TimeField(null=True, blank=True)
    wed_b_to_a = models.TimeField(null=True, blank=True)
    thurs_b_to_a = models.TimeField(null=True, blank=True)
    fri_b_to_a = models.TimeField(null=True, blank=True)
    sat_b_to_a = models.TimeField(null=True, blank=True)
    sun_b_to_a = models.TimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.allowed_route_id.status == "A":
            super(Preferred_Times, self).save(*args, **kwargs)
        else:
            raise Exception("You are not permitted to use this route yet sorry!")