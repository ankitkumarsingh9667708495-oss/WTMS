from django.urls import path
from . import views

urlpatterns = [
    path('', views.truck_list, name='truck_list'),
    path('add/', views.truck_create, name='truck_create'),
    path('edit/<int:pk>/', views.truck_edit, name='truck_edit'),
    path('delete/<int:pk>/', views.truck_delete, name='truck_delete'),
    path('drivers/', views.driver_list, name='driver_list'),
    path('drivers/add/', views.driver_create, name='driver_create'),
    path('drivers/edit/<int:pk>/', views.driver_edit, name='driver_edit'),
    path('drivers/delete/<int:pk>/', views.driver_delete,  name='driver_delete'),
]
