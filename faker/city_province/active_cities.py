import os
import sys

sys.path.append("/home/yottabyte/Desktop/Servers/anti_ncov/faker/")

from path import path_django
sys.path.append(path_django)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pasahero.settings')
import django
django.setup()

from django.db.models import Q
from cities.models import Cities


active_cities = Cities.objects.filter(Q(name="Lucena City") |
    Q(name="Angeles City") |
    Q(name="Meycauayan City") |
    Q(name="Bocaue") |
    Q(name="Quezon City") |
    Q(name="San Juan City") |
    Q(name="Makati") |
    Q(name="Santa Rosa City") |
    Q(name="Calamba City") |
    Q(name="Batangas City") |
    Q(name="Lipa City")
    )