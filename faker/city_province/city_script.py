import os
import sys

sys.path.append("/home/yottabyte/Desktop/Servers/anti_ncov/faker/")

from path import path_django
sys.path.append(path_django)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pasahero.settings')
import django
django.setup()

from random import random
from faker import Faker
from django.contrib.auth.models import User, Group
from cities.models import Provinces, Cities
from city_province.provinces_list import provinces
from city_province.cities_list import cities


# raise Exception("Have you already created provinces? And is there no existing cities entry?")


fakegen = Faker()
#convert provinces list to a dictionary for easy manipulation
provinces_dictionary = {}
for p in provinces:
    provinces_dictionary[p[0]] = p[1]

password_dictionary = {}
for c in cities:
    city_name = c[1]
    province_id = c[2]
    province_name = provinces_dictionary[province_id]
    province = Provinces.objects.get(name=province_name)
    tele_number = str(int(random()*10)) + str(int(random()*10)) + str(int(random()*10)) + str(int(random()*10)) + str(int(random()*10)) + str(int(random()*10)) + str(int(random()*10))
    phone_number = "09" + str(int(random()*10)) + str(int(random()*10)) + str(int(random()*10)) + str(int(random()*10)) + str(int(random()*10)) + str(int(random()*10)) + str(int(random()*10)) + str(int(random()*10)) + str(int(random()*10))

    password = fakegen.password()
    user =  User.objects.create_user(username=province_name+city_name,
                                 password=password)
    city_group = Group.objects.get(name='city')
    city_group.user_set.add(user)

    city = Cities(
        name=city_name,
        province_id=province,
        user_id=user,
        major_announcement=fakegen.sentence(),
        minor_announcement=fakegen.sentence(),
        major_is_active=fakegen.boolean(),
        minor_is_active=fakegen.boolean(),
        email=fakegen.email(),
        cell_number=phone_number,
        tele_number=tele_number,
    ).save()
    password_dictionary[province_name+city_name] = password

print(password_dictionary)