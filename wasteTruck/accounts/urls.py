from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name = "login"),
    path("logout/", views.logout_view, name = "logout"),
    path('admin-dashboard/', views.admin_dashboard, name = "admin_dashboard"),
    path('manage-user/', views.manage_user, name = 'manage_user'),
    path('staff-dashboard', views.staff_dashboard, name = 'staff_dashboard'),
    path('driver-dashboard', views.driver_dashboard, name= 'driver_dashboard'),
    path('manage-users/add/', views.user_create, name = 'user_create'),
    path('manage-users/<int:pk>/edit/', views.user_edit, name = 'user_edit'),
    path('manage-users/<int:pk>/delete/', views.user_delete, name = 'user_delete'),
]