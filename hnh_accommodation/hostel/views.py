from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Hostel
from .serializers import HostelSerializer


@api_view(['GET'])
def hostel_list(request):
    hostels = Hostel.objects.all()
    serializer = HostelSerializer(hostels, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def hostel_detail(request, hostel_id):
    try:
        hostel = Hostel.objects.get(id=hostel_id)
    except Hostel.DoesNotExist:
        return Response({'message': 'Hostel not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = HostelSerializer(hostel)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_hostel(request):
    serializer = HostelSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_hostel(request, hostel_id):
    try:
        hostel = Hostel.objects.get(id=hostel_id)
    except Hostel.DoesNotExist:
        return Response({'message': 'Hostel not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = HostelSerializer(hostel, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_hostel(request, hostel_id):
    try:
        hostel = Hostel.objects.get(id=hostel_id)
    except Hostel.DoesNotExist:
        return Response({'message': 'Hostel not found'}, status=status.HTTP_404_NOT_FOUND)

    hostel.delete()
    return Response({'message': 'Hostel deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
