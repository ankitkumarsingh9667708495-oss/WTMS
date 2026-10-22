from django import forms
from django.db.models import Q
from .models import Truck, Driver, CollectionAssignment


class TruckForm(forms.ModelForm):
    class Meta:
        model = Truck
        fields = [
            'truck_number',
            'truck_type',
            'capacity',
            'status',
            'compatible_waste_type',
            'fuel_type',
            'puc',
            'assigned_driver',
        ]
        widgets = {
            'puc': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Show active drivers who are not assigned to a truck.
        available_drivers = Driver.objects.filter(
            status='active',
            assigned_truck__isnull=True
        )

        # When editing, retain this truck's current driver.
        if self.instance.pk and self.instance.assigned_driver_id:
            available_drivers = (
                available_drivers
                | Driver.objects.filter(
                    pk=self.instance.assigned_driver_id
                )
            ).distinct()

        self.fields['assigned_driver'].queryset = (
            available_drivers.order_by('full_name')
        )
        self.fields['assigned_driver'].required = False

    def clean_assigned_driver(self):
        driver = self.cleaned_data.get('assigned_driver')

        if driver is None:
            return driver

        # Don't allow assigning an inactive driver for the first time.
        current_driver_id = (
            self.instance.assigned_driver_id
            if self.instance.pk else None
        )

        if driver.status != 'active' and driver.pk != current_driver_id:
            raise forms.ValidationError(
                'Only active drivers can be assigned to a truck.'
            )

        # Prevent assigning a driver who belongs to another truck.
        other_trucks = Truck.objects.filter(
            assigned_driver=driver
        )

        if self.instance.pk:
            other_trucks = other_trucks.exclude(
                pk=self.instance.pk
            )

        if other_trucks.exists():
            raise forms.ValidationError(
                'This driver is already assigned to another truck.'
            )

        return driver


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = [
            'full_name',
            'phone',
            'license_number',
            'license_expiry',
            'address',
            'status',
        ]

        widgets = {
            'license_expiry': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'address': forms.Textarea(
                attrs={'rows': 3}
            ),
        }

class CollectionAssignmentForm(forms.ModelForm):
    class Meta:
        model = CollectionAssignment
        fields = ['driver', 'truck', 'route', 'scheduled_date']
        widgets = {
            'scheduled_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'route': forms.TextInput(attrs={
                'placeholder': 'e.g. Sector 62, Noida'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        busy_driver_ids = CollectionAssignment.objects.filter(
        status__in=['assigned', 'in_progress']
        ).values_list('driver_id', flat=True)

        drivers_with_trucks = Truck.objects.filter(
            assigned_driver__isnull=False
        ).values_list('assigned_driver_id', flat=True)

        self.fields['driver'].queryset = Driver.objects.filter(
            status='active'
        ).exclude(
            id__in=busy_driver_ids
        ).exclude(
            id__in=drivers_with_trucks
        ).order_by('full_name')
