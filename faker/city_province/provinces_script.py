import os
import sys

sys.path.append("/home/yottabyte/Desktop/Servers/anti_ncov/faker/")

from path import path_django
sys.path.append(path_django)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pasahero.settings')
import django
django.setup()

from cities.models import Provinces
from city_province.provinces_list import provinces

# raise Exception("Is your database already populated with provinces? If so DO NOT rerun me.")
print('About to populate database with provinces')
for p in provinces:
    Provinces(name=p[1]).save()
print('All provinces of the Philippines have been entered into the database')