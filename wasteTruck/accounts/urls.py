from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name = "login"),
    path("logout/", views.logout_view, name = "logout"),
    path('register/', views.register_view, name = 'register'),
    path('admin-dashboard/', views.admin_dashboard, name = "admin_dashboard"),
    path('manage)user.html', views.manage_user, name = 'manage_user'),
    path('staff-dashboard', views.staff_dashboard, name = 'staff_dashboard'),
    path('driver-dashboard', views.driver_dashboard, name= 'driver_dashboard'),
]
