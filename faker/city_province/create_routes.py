import os
import sys

sys.path.append("/home/yottabyte/Desktop/Servers/anti_ncov/faker/")

from path import path_django
sys.path.append(path_django)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pasahero.settings')
import django
django.setup()

from faker import Faker
from django.contrib.auth.models import User, Group
from transportations.models import Routes
from cities.models import Cities
from city_province.active_cities import active_cities


# raise Exception("Are you sure you want to make 10 routes?")

fakegenSpan = Faker('es_ES')



for city in active_cities:
    for x in range(5):
        place = fakegenSpan.address().split()
        a = place[0]
        b = place[2]
        via = fakegenSpan.address().split()[0]
        employee = city.employees.get()

        Routes(city_id=city,
                    province_id=city.province_id,
                    employee_id=employee,
                    name=a + " - "+ b,
                    via=via,
                    is_active=True,
                    point_a=a,
                    point_b=b,
                ).save()