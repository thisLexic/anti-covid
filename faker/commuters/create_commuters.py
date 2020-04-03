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
from commuters.models import Commuters
from cities.models import Cities
from city_province.active_cities import active_cities

raise Exception("Are you sure you wana make 100 more commuters for Lucena City?")

fakegenSpan = Faker('es_ES')
fakegenEng = Faker('en_US')

jobs = ['Nurse', 'Doctor', "Pharmacist", "Security Guard", "IT", "Cashier", "Teller", 'Janitor', "Manager", "Technician"]
companies = ['Puregold', "The Generics Pharmacy", "BDO", "Power Plant", "Meralco", "Happy Hospital", "Cachow Clinic"]

commuter_group = Group.objects.get(name='commuter')

for x in range(0,20):
    user =  User.objects.create_user(username="c"+str(x), password="0000")
    commuter_group.user_set.add(user)
    city_work = random.choice(active_cities)
    city_live = random.choice(active_cities)

    name = fakegenEng.name().split()

    commuter = Commuters(
        lives_city_id=city_live,
        works_city_id=city_work,
        lives_province_id=city_live.province_id,
        works_province_id=city_work.province_id,
        user_id=user,
        preferred_pick_up=fakegenSpan.address(),
        last_name=name[1],
        first_name=name[0],
        middle_name=name[1],
        profession=random.choice(jobs),
        company_name=random.choice(companies),
        company_location=fakegenSpan.address(),
        present_address=fakegenSpan.address(),
        permanent_address=fakegenSpan.address(),
        ).save()