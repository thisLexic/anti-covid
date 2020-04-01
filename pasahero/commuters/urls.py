from django.urls import path
from . import views

app_name = "commuters"

urlpatterns = [
    path('submit/', views.create_commuter, name='create_commuter'),

    path('announcements/', views.AnnouncementsList.as_view(), name='announcements'),

    path('edit/<int:pk>', views.CommuterUpdate.as_view(), name='edit_commuter'),

    path('view/my_routes/', views.view_my_routes, name="view_my_routes"),

    path('apply/route', views.find_route, name="apply_city"),
    path('apply/trip/<int:pk>', views.apply_route, name="apply_route"),
    path('apply/trip/confirm/<int:pk>', views.apply_route_action, name="apply_route_action"),

    path('ajax/load-lives-cities/', views.load_lives_cities, name='ajax_load_lives_cities'),
    path('ajax/load-works-cities/', views.load_works_cities, name='ajax_load_works_cities'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
]