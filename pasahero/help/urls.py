from django.urls import path
from . import views

app_name = "help"

urlpatterns = [
    path('', views.home, name='home'),
    path('pasahero/', views.pasahero, name='pasahero'),
    path('admin/', views.admin, name='admin'),
    path('super-admin/', views.super_admin, name='superadmin'),
]
