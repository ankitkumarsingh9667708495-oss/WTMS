
from django.urls import path
from . import api_views

urlpatterns = [
    path('trucks/', api_views.truck_api_list, name='truck_api_list'),
    path('trucks/create/', api_views.truck_api_create, name = 'truck_api_create'),
    path('trucks/<int:pk>/update/', api_views.truck_api_update, name='truck_api_update'),
    path('trucks/<int:pk>/partial-update/', api_views.truck_api_partial_update, name='truck_api_partial_update'),
    path('trucks/<int:pk>/delete/', api_views.truck_api_delete, name='truck_api_delete'),
    path('drivers/', api_views.driver_api_list, name='driver_api_list'),
    path('drivers/create/', api_views.driver_api_create, name='driver_api_create'),
    path('drivers/<int:pk>/update/', api_views.driver_api_update, name='driver_api_update'),
    path('drivers/<int:pk>/partial-update/', api_views.driver_api_partial_update, name='driver_api_partial_update'),
    path('drivers/<int:pk>/delete/', api_views.driver_api_delete, name='driver_api_delete'),
    path('assignments/', api_views.assignment_api_list, name='assignment_api_list'),
    path('assignments/create/', api_views.assignment_api_create, name='assignment_api_create'),
    path('assignments/<int:pk>/update/', api_views.assignment_api_update, name='assignment_api_update'),
    path('assignments/<int:pk>/partial-update/', api_views.assignment_api_partial_update, name='assignment_api_partial_update'),
    path('assignments/<int:pk>/delete/', api_views.assignment_api_delete, name='assignment_api_delete'),
    path('dashboard/stats/', api_views.dashboard_stats_api, name='dashboard_stats_api'),
    path('dashboard/activities/', api_views.dashboard_activities_api, name='dashboard_activities_api'),
    path('driver/profile/', api_views.driver_profile_api, name='driver_profile_api'),
    path('driver/my-assignments/', api_views.my_assignments_api, name='my_assignments_api'),
    path('driver/my-assignments/<int:pk>/', api_views.my_assignment_detail_api, name='my_assignment_detail_api'),
    path('driver/my-assignments/<int:pk>/update-status/', api_views.driver_update_assignment_status_api, name='driver_update_assignment_status_api'),
]
