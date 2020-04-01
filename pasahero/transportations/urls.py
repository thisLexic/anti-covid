from django.urls import path
from . import views

app_name = "transportations"

urlpatterns = [
    path('view/cities/', views.view_cities, name="view_cities"),
    path('view/routes/<int:pk>', views.view_routes, name="view_routes"),
    path('view/directions/<int:pk>', views.view_directions, name="view_directions"),
    path('view/allowed_routes/',views.view_allowed_routes, name="view_allowed_routes"),
    path('view/allowed_commuters/',views.view_allowed_commuters, name="view_allowed_commuters"),
    path('view/my_routes/', views.view_my_routes, name="view_my_routes"),
]