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

    assigned_driver = models.OneToOneField(
        'Driver',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_truck'
    )

    
    @property
    def is_available(self):
        return (
            self.status == 'active'
            and self.assigned_driver is None
        )


    def __str__(self):
        return self.truck_number


class Driver(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    license_number = models.CharField(max_length=30, unique=True)
    license_expiry = models.DateField()
    address = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_available(self):
        if self.status != 'active':
            return False

        try:
            self.assigned_truck
            return False
        except Truck.DoesNotExist:
            return True


    def __str__(self):
        return self.full_name
