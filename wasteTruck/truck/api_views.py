from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrStaff, IsAdminOnly

from .models import Truck
from .serializers import TruckSerializer


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