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
from city_province.active_cities import active_cities
from transportations.models import Routes
from cities.models import Cities
from employees.models import Employees

fakeSpan = Faker('es_ES')
fakeEng = Faker('en_US')

# raise Exception("Are you sure you want to generate 1 employee for each active city?")

employee_group = Group.objects.get(name='employee')
number = 0
jobs=['Administrative Officer', "Manager", "Clerk", "Accountant", "Treasurer", "Intern"]
departments=["Finance", "Public Relations", "Logistics", "Marketing", "Information Technology"]
for city in active_cities:
    user =  User.objects.create_user(username="e"+str(number), password="0000")
    employee_group.user_set.add(user)
    name = fakeEng.name().split()

    Employees(user_id=user,
        city_id=city,
        last_name=name[1],
        first_name=name[0],
        job_title=random.choice(jobs),
        department=random.choice(departments),
    ).save()

    number += 1