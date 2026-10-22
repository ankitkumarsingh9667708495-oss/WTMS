from django.contrib import admin
from .models import Truck, Driver, CollectionAssignment

# Register your models here.

admin.site.register(Truck)
admin.site.register(Driver)
admin.site.register(CollectionAssignment)