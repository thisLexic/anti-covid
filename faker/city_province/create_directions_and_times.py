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
from transportations.models import Routes, Directions, Times

# raise Exception("Are you sure you want to generate random directions and times for all routes without directions yet?")

count = 0
vehicles = ["Jeep", "Bus", "UV Express", "Van"]
times_minutes = ["10","15","30","45","60","120","120"]
numbers = [1,2,3,4,5,6,7,8,9,10,11,12]
capacity = [10,20,40,60,80,100,120,150,200]
routes = Routes.objects.filter(directions__isnull=True)
for route in routes:
    point_a = route.point_a
    point_b = route.point_b

    direction_a = Directions(
        route_id=route,
        start_location=point_a,
        end_location=point_b,
        vehicle=random.choice(vehicles),
        duration_minutes=random.choice(times_minutes),
    )

    direction_b = Directions(
        route_id=route,
        start_location=point_b,
        end_location=point_a,
        vehicle=random.choice(vehicles),
        duration_minutes=random.choice(times_minutes),
    )

    direction_a.save()
    direction_b.save()

    for x in range(random.choice(numbers)):
        try:
            count+=1
            Times(
                direction_id=direction_a,
                time=random.choice(TIME_SELECTIONS)[0],
                capacity=random.choice(capacity)
            ).save()
        except:
            pass
    for x in range(random.choice(numbers)):
        try:
            count+=1
            Times(
                direction_id=direction_b,
                time=random.choice(TIME_SELECTIONS)[0],
                capacity=random.choice(capacity)
            ).save()
        except:
            pass
            
print(count)