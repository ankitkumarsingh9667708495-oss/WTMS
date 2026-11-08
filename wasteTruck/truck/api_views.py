from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrStaff, IsAdminOnly, IsDriver
from .models import Truck, Driver, CollectionAssignment, Activity
from .serializers import TruckSerializer, DriverSerializer, CollectionAssignmentSerializer
from .forms import CollectionAssignmentForm
from django.db import transaction
from django.utils import timezone
from django.db.models import Count, Q


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminOrStaff])
def truck_api_list(request):
    trucks = Truck.objects.all().order_by('truck_number')

    serializer = TruckSerializer(trucks, many=True)

    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminOrStaff])
def truck_api_create(request):

    serializer = TruckSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response(
            serializer.data,
            status=201
        )

    return Response(
        serializer.errors,
        status=400
    )


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminOrStaff])
def truck_api_update(request, pk):

    try:
        truck = Truck.objects.get(pk=pk)
    except Truck.DoesNotExist:
        return Response(
            {'error': 'Truck not found.'},
            status=404
        )

    serializer = TruckSerializer(
        truck,
        data=request.data
    )

    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data)

    return Response(
        serializer.errors,
        status=400
    )

@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminOrStaff])
def truck_api_partial_update(request, pk):

    try:
        truck = Truck.objects.get(pk=pk)
    except Truck.DoesNotExist:
        return Response(
            {'error': 'Truck not found.'},
            status=404
        )

    serializer = TruckSerializer(
        truck,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(
        serializer.errors,
        status=400
    )

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminOnly])
def truck_api_delete(request, pk):

    try:
        truck = Truck.objects.get(pk=pk)
    except Truck.DoesNotExist:
        return Response(
            {'error': 'Truck not found.'},
            status=404
        )

    truck.delete()

    return Response(
        {'message': 'Truck deleted successfully.'},
        status=200
    )

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminOrStaff])
def driver_api_list(request):

    drivers = Driver.objects.all().order_by('full_name')

    serializer = DriverSerializer(drivers, many=True)

    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminOrStaff])
def driver_api_create(request):

    serializer = DriverSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminOrStaff])
def driver_api_update(request, pk):

    try:
        driver = Driver.objects.get(pk=pk)
    except Driver.DoesNotExist:
        return Response(
            {'error': 'Driver not found.'},
            status=404
        )

    serializer = DriverSerializer(
        driver,
        data=request.data
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(
        serializer.errors,
        status=400
    )

@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminOrStaff])
def driver_api_partial_update(request, pk):

    try:
        driver = Driver.objects.get(pk=pk)
    except Driver.DoesNotExist:
        return Response(
            {'error': 'Driver not found.'},
            status=404
        )

    serializer = DriverSerializer(
        driver,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(
        serializer.errors,
        status=400
    )

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminOnly])
def driver_api_delete(request, pk):

    try:
        driver = Driver.objects.get(pk=pk)
    except Driver.DoesNotExist:
        return Response(
            {'error': 'Driver not found.'},
            status=404
        )

    driver.delete()

    return Response(
        {'message': 'Driver deleted successfully.'},
        status=200
    )

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminOrStaff])
def assignment_api_list(request):

    assignments = CollectionAssignment.objects.all().order_by('-created_at')

    serializer = CollectionAssignmentSerializer(
        assignments,
        many=True
    )

    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminOrStaff])
def assignment_api_create(request):

    form = CollectionAssignmentForm(request.data)

    if form.is_valid():

        with transaction.atomic():

            driver = Driver.objects.select_for_update().get(
                pk=form.cleaned_data['driver'].pk
            )

            truck = Truck.objects.select_for_update().get(
                pk=form.cleaned_data['truck'].pk
            )

            if driver.status != 'active':
                return Response(
                    {'driver': ['Driver is inactive.']},
                    status=400
                )

            if driver.license_expiry < timezone.localdate():
                return Response(
                    {'driver': ['Driver licence has expired.']},
                    status=400
                )

            if truck.status != 'active':
                return Response(
                    {'truck': ['Truck is inactive.']},
                    status=400
                )

            if Truck.objects.filter(assigned_driver=driver).exists():
                return Response(
                    {'driver': ['Driver is already assigned to a truck.']},
                    status=400
                )

            if CollectionAssignment.objects.filter(
                driver=driver,
                status__in=['assigned', 'in_progress']
            ).exists():
                return Response(
                    {'driver': ['Driver already has an ongoing collection.']},
                    status=400
                )

            if truck.assigned_driver_id is not None:
                return Response(
                    {'truck': ['Truck is already assigned to a driver.']},
                    status=400
                )

            if CollectionAssignment.objects.filter(
                truck=truck,
                status__in=['assigned', 'in_progress']
            ).exists():
                return Response(
                    {'truck': ['Truck already has an ongoing collection.']},
                    status=400
                )

            assignment = form.save(commit=False)
            assignment.driver = driver
            assignment.truck = truck
            assignment.save()

            truck.assigned_driver = driver
            truck.save(update_fields=['assigned_driver'])

        serializer = CollectionAssignmentSerializer(assignment)

        return Response(serializer.data, status=201)

    return Response(form.errors, status=400)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminOrStaff])
def assignment_api_update(request, pk):

    try:
        assignment = CollectionAssignment.objects.get(pk=pk)
    except CollectionAssignment.DoesNotExist:
        return Response(
            {'error': 'Assignment not found.'},
            status=404
        )

    # Preserve the existing assignment status.
    original_status = assignment.status

    # Validate the submitted data using the existing form.
    form = CollectionAssignmentForm(request.data)

    if not form.is_valid():
        return Response(form.errors, status=400)

    with transaction.atomic():

        driver = Driver.objects.select_for_update().get(
            pk=form.cleaned_data['driver'].pk
        )

        truck = Truck.objects.select_for_update().get(
            pk=form.cleaned_data['truck'].pk
        )

        # Check driver availability.
        if driver.status != 'active':
            return Response(
                {'driver': ['Driver is inactive.']},
                status=400
            )

        if driver.license_expiry < timezone.localdate():
            return Response(
                {'driver': ['Driver licence has expired.']},
                status=400
            )

        if Truck.objects.filter(
            assigned_driver=driver
        ).exclude(pk=truck.pk).exists():
            return Response(
                {'driver': ['Driver is already assigned to another truck.']},
                status=400
            )

        if CollectionAssignment.objects.filter(
            driver=driver,
            status__in=['assigned', 'in_progress']
        ).exclude(pk=assignment.pk).exists():
            return Response(
                {'driver': ['Driver already has another ongoing collection.']},
                status=400
            )

        # Check truck availability.
        if truck.status != 'active':
            return Response(
                {'truck': ['Truck is inactive.']},
                status=400
            )

        if truck.assigned_driver_id not in [None, driver.pk]:
            return Response(
                {'truck': ['Truck is already assigned to another driver.']},
                status=400
            )

        if CollectionAssignment.objects.filter(
            truck=truck,
            status__in=['assigned', 'in_progress']
        ).exclude(pk=assignment.pk).exists():
            return Response(
                {'truck': ['Truck already has another ongoing collection.']},
                status=400
            )

        # Remember the old truck.
        old_truck = assignment.truck
        old_driver = assignment.driver

        # Update assignment details.
        assignment.driver = driver
        assignment.truck = truck
        assignment.route = form.cleaned_data['route']
        assignment.scheduled_date = form.cleaned_data['scheduled_date']
        assignment.status = original_status

        assignment.save()

        # Release the old truck if it is no longer being used
        # by this driver for an ongoing assignment.
        if old_truck.pk != truck.pk or old_driver.pk != driver.pk:

            if not CollectionAssignment.objects.filter(
                truck=old_truck,
                status__in=['assigned', 'in_progress']
            ).exclude(pk=assignment.pk).exists():

                if old_truck.assigned_driver_id == old_driver.pk:
                    old_truck.assigned_driver = None
                    old_truck.save(update_fields=['assigned_driver'])
        
        # Link the new driver to the new truck.
        truck.assigned_driver = driver
        truck.save(update_fields=['assigned_driver'])

    serializer = CollectionAssignmentSerializer(assignment)

    return Response(serializer.data, status=200)


@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminOrStaff])
def assignment_api_partial_update(request, pk):

    with transaction.atomic():
        try:
            assignment = CollectionAssignment.objects.select_for_update().select_related(
                'truck', 'driver'
            ).get(pk=pk)
        except CollectionAssignment.DoesNotExist:
            return Response(
                {'error': 'Assignment not found.'},
                status=404
            )

        new_status = request.data.get('status')

        allowed_transitions = {
            'assigned': ['in_progress'],
            'in_progress': ['completed'],
            'completed': [],
        }

        if new_status not in allowed_transitions.get(assignment.status, []):
            return Response(
                {'error': 'Invalid assignment status change.'},
                status=400
            )

        assignment.status = new_status
        assignment.save(update_fields=['status'])

        if new_status == 'completed':
            truck = Truck.objects.select_for_update().get(
                pk=assignment.truck_id
            )

            other_active_assignments = CollectionAssignment.objects.filter(
                truck_id=assignment.truck_id,
                status__in=['assigned', 'in_progress']
            ).exclude(pk=assignment.pk)

            if (
                not other_active_assignments.exists()
                and truck.assigned_driver_id == assignment.driver_id
            ):
                truck.assigned_driver = None
                truck.save(update_fields=['assigned_driver'])

            Activity.objects.create(
                action='collection_completed',
                description=(
                    f'{assignment.driver.full_name} completed the collection '
                    f'for route {assignment.route} using truck '
                    f'{truck.truck_number}.'
                ),
                driver=assignment.driver
            )
        serializer = CollectionAssignmentSerializer(assignment)
        return Response(serializer.data, status=200)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminOnly])
def assignment_api_delete(request, pk):

    with transaction.atomic():

        try:
            assignment = CollectionAssignment.objects.select_for_update().select_related(
                'truck', 'driver'
            ).get(pk=pk)

        except CollectionAssignment.DoesNotExist:
            return Response(
                {'error': 'Assignment not found.'},
                status=404
            )

        truck = Truck.objects.select_for_update().get(
            pk=assignment.truck_id
        )

        # Release the truck if it is assigned to this driver.
        if truck.assigned_driver_id == assignment.driver_id:
            truck.assigned_driver = None
            truck.save(update_fields=['assigned_driver'])

        assignment.delete()

    return Response(
        {'message': 'Collection assignment deleted successfully.'},
        status=200
    )


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminOrStaff])
def dashboard_stats_api(request):

    total_trucks = Truck.objects.count()
    active_trucks = Truck.objects.filter(status='active').count()

    total_drivers = Driver.objects.count()
    active_drivers = Driver.objects.filter(status='active').count()

    total_assignments = CollectionAssignment.objects.count()

    completed_assignments = CollectionAssignment.objects.filter(
        status='completed'
    ).count()

    pending_assignments = CollectionAssignment.objects.filter(
        status='assigned'
    ).count()

    in_progress_assignments = CollectionAssignment.objects.filter(
        status='in_progress'
    ).count()

    completion_percentage = (
        round((completed_assignments / total_assignments) * 100, 2)
        if total_assignments > 0 else 0
    )

    data = {
        'trucks': {
            'total': total_trucks,
            'active': active_trucks,
        },
        'drivers': {
            'total': total_drivers,
            'active': active_drivers,
        },
        'assignments': {
            'total': total_assignments,
            'completed': completed_assignments,
            'pending': pending_assignments,
            'in_progress': in_progress_assignments,
        },
        'completion_percentage': completion_percentage,
    }

    return Response(data, status=200)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminOrStaff])
def dashboard_activities_api(request):

    activities = Activity.objects.all().order_by('-created_at')[:5]

    data = []

    for activity in activities:
        data.append({
            'id': activity.id,
            'action': activity.action,
            'description': activity.description,
            'created_at': activity.created_at,
        })

    return Response(data, status=200)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsDriver])
def driver_profile_api(request):

    try:
        driver = request.user.driver_profile
    except Driver.DoesNotExist:
        return Response(
            {'error': 'Driver profile not found.'},
            status=404
        )

    serializer = DriverSerializer(driver)

    return Response(serializer.data, status=200)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsDriver])
def my_assignments_api(request):

    driver = request.user.driver_profile

    assignments = CollectionAssignment.objects.filter(
        driver=driver
    ).select_related('truck', 'driver').order_by('-created_at')

    serializer = CollectionAssignmentSerializer(
        assignments,
        many=True
    )

    return Response(serializer.data, status=200)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsDriver])
def my_assignment_detail_api(request, pk):

    try:
        assignment = CollectionAssignment.objects.select_related(
            'truck', 'driver'
        ).get(
            pk=pk,
            driver=request.user.driver_profile
        )

    except CollectionAssignment.DoesNotExist:
        return Response(
            {'error': 'Assignment not found.'},
            status=404
        )

    serializer = CollectionAssignmentSerializer(assignment)

    return Response(serializer.data, status=200)


@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsDriver])
def driver_update_assignment_status_api(request, pk):

    with transaction.atomic():
        try:
            assignment = CollectionAssignment.objects.select_for_update().select_related(
                'truck', 'driver'
            ).get(
                pk=pk,
                driver=request.user.driver_profile
            )

        except CollectionAssignment.DoesNotExist:
            return Response(
                {'error': 'Assignment not found.'},
                status=404
            )

        new_status = request.data.get('status')

        allowed_transitions = {
            'assigned': ['in_progress'],
            'in_progress': ['completed'],
            'completed': [],
        }

        if new_status not in allowed_transitions.get(assignment.status, []):
            return Response(
                {'error': 'Invalid assignment status change.'},
                status=400
            )

        assignment.status = new_status
        assignment.save(update_fields=['status'])

        if new_status == 'completed':

            truck = Truck.objects.select_for_update().get(
                pk=assignment.truck_id
            )

            other_active_assignments = CollectionAssignment.objects.filter(
                truck_id=assignment.truck_id,
                status__in=['assigned', 'in_progress']
            ).exclude(pk=assignment.pk)

            if (
                not other_active_assignments.exists()
                and truck.assigned_driver_id == assignment.driver_id
            ):
                truck.assigned_driver = None
                truck.save(update_fields=['assigned_driver'])

                Activity.objects.create(
                    action='collection_completed',
                    description=(
                        f'{assignment.driver.full_name} completed the collection '
                        f'for route {assignment.route} using truck '
                        f'{truck.truck_number}.'
                    )
                )

        serializer = CollectionAssignmentSerializer(assignment)

        return Response(serializer.data, status=200)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsDriver])
def driver_dashboard_stats_api(request):

    driver = request.user.driver_profile

    total_assignments = CollectionAssignment.objects.filter(
        driver=driver
    ).count()

    pending_assignments = CollectionAssignment.objects.filter(
        driver=driver,
        status='assigned'
    ).count()

    in_progress_assignments = CollectionAssignment.objects.filter(
        driver=driver,
        status='in_progress'
    ).count()

    completed_assignments = CollectionAssignment.objects.filter(
        driver=driver,
        status='completed'
    ).count()

    data = {
        'total_assignments': total_assignments,
        'pending_assignments': pending_assignments,
        'in_progress_assignments': in_progress_assignments,
        'completed_assignments': completed_assignments,
    }

    return Response(data, status=200)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsDriver])
def driver_dashboard_activities_api(request):

    driver = request.user.driver_profile

    activities = Activity.objects.filter(
        driver=driver
    ).order_by('-created_at')[:5]

    data = []

    for activity in activities:
        data.append({
            'id': activity.id,
            'action': activity.action,
            'description': activity.description,
            'created_at': activity.created_at,
        })

    return Response(data, status=200)