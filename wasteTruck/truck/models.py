from django.db import models

# Create your models here.

class Truck(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Maintenance')
    ]

    FUEL_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric')
    ]

    WASTE_CHOICES = [
        ('dry', 'Dry Waste'),
        ('wet', 'Wet Waste'),
        ('plastic', 'Plastic'),
        ('mixed', 'Mixed Waste')
    ]

    truck_number = models.CharField(max_length=20, unique=True)
    truck_type = models.CharField(max_length=20)
    capacity = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    compatible_waste_type = models.CharField(max_length=20, choices=WASTE_CHOICES)
    fuel_type = models.CharField(max_length=20, choices= FUEL_CHOICES)
    puc = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.truck_number