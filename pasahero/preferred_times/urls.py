from django.urls import path
from . import views

app_name = "preferred_times"

urlpatterns = [
    path('', views.view_allowed_routes, name='list'),
    path('redirect/<int:pk>', views.UpdateCreateRedirectView.as_view(), name='edit'),
    path('create/<int:pk>', views.Create.as_view(), name='create'),
    path('update/<int:pk>', views.Update.as_view(), name='update'),
]