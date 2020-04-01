from django.urls import path
from . import views

app_name = "cities"

urlpatterns = [
    path('', views.home, name='home_page'),
    path('login/', views.login_city, name='login'),

    path('change-password/', views.change_password, name='change_password'),

    path('announcement/', views.UpdateAnnouncement.as_view(), name='announcement_edit'),

    path('employees/', views.EmployeesList.as_view(), name='employees_list'),
    path('employee/detail/<int:pk>', views.EmployeeDetail.as_view(), name='employee_details'),
    path('employee/add/', views.create_employee, name='add'),
    path('employee/change/<int:pk>', views.employee_change, name='employee_change'),

    path('routes/list/', views.RoutesList.as_view(), name='list_routes'),
    path('routes/delete/<int:pk>', views.delete_route, name='delete_route'),
]