from django.contrib import admin
from .models import Commuters, Allowed_Routes

admin.site.register(Commuters)
admin.site.register(Allowed_Routes)
