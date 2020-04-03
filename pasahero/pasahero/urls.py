from django.contrib import admin
from django.urls import path, include
from . import views

from pasahero import settings
if settings.DEBUG:
    from django.contrib.staticfiles.urls import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', views.login_user,name="login"),
    path('logout/', views.logout_user,name="logout"),
    path('signup/', views.signup_user,name='signup'),

    path('', views.home, name='home'),
    path('drivers/', views.drivers, name='drivers'),
    path('about/', views.about, name='about'),

    path('transportations/', include('transportations.urls', namespace='transportations')),
    path('commuters/', include('commuters.urls', namespace='commuters')),
    path('documents/', include('documents.urls', namespace='documents')),
    path('manage/', include('cities.urls', namespace='cities')),
    path('employee/', include('employees.urls', namespace='employees')),
    path('preferred-times/', include('preferred_times.urls', namespace='preferred_times')),
    path('help/', include('help.urls', namespace='help')),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)