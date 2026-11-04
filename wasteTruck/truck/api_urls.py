
from django.urls import path
from . import api_views

urlpatterns = [
    path('trucks/', api_views.truck_api_list, name='truck_api_list'),
    path('trucks/create/', api_views.truck_api_create, name = 'truck_api_create'),
    path('trucks/<int:pk>/update/', api_views.truck_api_update, name='truck_api_update'),
    path('trucks/<int:pk>/partial-update/', api_views.truck_api_partial_update, name='truck_api_partial_update'),
    path('trucks/<int:pk>/delete/', api_views.truck_api_delete, name='truck_api_delete'),
]
