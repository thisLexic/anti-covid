from django.urls import path
from . import views

app_name = "documents"

urlpatterns = [
    path('read/', views.read, name='read'),
    path('create/', views.CreateDocument.as_view(), name='create'),
    path('detail/<int:pk>', views.DetailDocument.as_view(), name='detail'),
    path('edit/<int:pk>', views.UpdateDocument.as_view(), name='edit_document'),
    path('delete/<int:pk>', views.DeleteDocument.as_view(), name='delete_document'),
]
