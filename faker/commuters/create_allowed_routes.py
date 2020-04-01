import os
import sys

sys.path.append("/home/yottabyte/Desktop/Servers/anti_ncov/faker/")

from path import path_django
sys.path.append(path_django)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pasahero.settings')
import django
django.setup()

import random
from faker import Faker
from django.contrib.auth.models import User, Group
from commuters.models import Allowed_Routes, Commuters
from transportations.models import Routes

raise Exception("Are you sure you wana make almost 300 allowed routes?")

fakegenSpan = Faker('es_ES')

routes = Routes.objects.all()
commuters = Commuters.objects.all()
status = ["A","P","R"]

valid=0
for commuter in commuters:
    for x in range(0,10):
        try:
            route = random.choice(routes)
            employee = route.city_id.employees.get()
            Allowed_Routes(
                route_id=route,
                commuter_id=commuter,
                employee_id=employee,
                status=random.choice(status),
                ).save()
            valid+=1
        except:
            pass
print(valid)