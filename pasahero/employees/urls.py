from django.urls import path
from . import views

app_name = "employees"

urlpatterns = [
    path('', views.home_page, name='home_page'),

    path('announcements/', views.announcements, name='announcement'),

    path('routes/active', views.ListActiveRoutes.as_view(), name='active'),
    path('routes/inactive', views.ListInactiveRoutes.as_view(), name='inactive'),
    path('route/details/<int:pk>', views.RouteDetail.as_view(), name='details_route'),
    path('route/applicants/<int:pk>/<slug:status>/', views.CommutersList.as_view(), name='commuters_list'),
    path('route/pdf/<int:pk>/<slug:status>/', views.pdf, name='pdf'),
    path('route/preferred-time/<int:pk>/<slug:flip>', views.employee_preferred_time, name='employee_preferred_time'),

    path('commuter/detail/<int:pk>/<int:pk_ar>/', views.CommuterDetail.as_view(), name='commuter_detail'),
    path('commuter/decide/<int:pk_ar>/<int:pk_route>/<slug:old_status>/<slug:new_status>/', views.decision_commuter, name='decision_commuter'),
    path('commuter/document/<int:doc_pk>/<int:route_pk>/', views.DocumentDetail.as_view(), name='commuter_document'),

    path('route/add', views.CreateRoute.as_view(), name='add'),
    path('route/update/<int:pk>', views.change_status_route, name='change_status_route'),

    path('directions/add/<int:pk>', views.add_directions, name='add_directions'),
    path('directions/edit/<int:route_pk>/<int:dir_pk>', views.edit_directions, name='edit_directions'),
    path('directions/delete/<int:route_pk>/<int:dir_pk>', views.delete_direction, name='delete_direction'),

    path('times/add/<int:dir_pk>', views.add_times, name='add_times'),
    path('times/list/<int:dir_pk>', views.TimesList.as_view(), name='list_times'),
    path('times/delete/<int:dir_pk>/<int:t_pk>', views.time_delete, name='time_delete'),

    path('change-password/', views.change_password, name='change_password'),
]