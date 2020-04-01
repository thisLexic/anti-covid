import os
import sys

sys.path.append("/home/yottabyte/Desktop/Servers/anti_ncov/faker/")

from path import path_django
sys.path.append(path_django)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pasahero.settings')
import django
django.setup()

import random
from datetime import datetime
from faker import Faker
from django.contrib.auth.models import User, Group
from times import TIME_SELECTIONS
from commuters.models import Allowed_Routes
from preferred_times.models import Preferred_Times

# raise Exception("Are you sure you want to generate random preferred times for all commuters?")


ars = Allowed_Routes.objects.filter(status="A",preferred_time__isnull=True)

count = 0
for ar in ars:
    Preferred_Times(
        allowed_route_id=ar,
        mon_a_to_b = random.choice(TIME_SELECTIONS)[0],
        tues_a_to_b = random.choice(TIME_SELECTIONS)[0],
        wed_a_to_b = random.choice(TIME_SELECTIONS)[0],
        thurs_a_to_b = random.choice(TIME_SELECTIONS)[0],
        fri_a_to_b = random.choice(TIME_SELECTIONS)[0],
        sat_a_to_b = random.choice(TIME_SELECTIONS)[0],
        sun_a_to_b = random.choice(TIME_SELECTIONS)[0],
        mon_b_to_a = random.choice(TIME_SELECTIONS)[0],
        tues_b_to_a = random.choice(TIME_SELECTIONS)[0],
        wed_b_to_a = random.choice(TIME_SELECTIONS)[0],
        thurs_b_to_a = random.choice(TIME_SELECTIONS)[0],
        fri_b_to_a = random.choice(TIME_SELECTIONS)[0],
        sat_b_to_a = random.choice(TIME_SELECTIONS)[0],
        sun_b_to_a = random.choice(TIME_SELECTIONS)[0],
    ).save()
    count += 1
print(count)