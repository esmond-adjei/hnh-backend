from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from .models import Hostel, Room
from .serializers import HostelSerializer, RoomSerializer
from .filters import HostelFilter, RoomFilter
from django.db.models import Q


# -------------------------- SEARCH VIEWS --------------------------
@api_view(['GET'])
@permission_classes([AllowAny])
def search_hostels(request):
    search_query = request.query_params.get('q', None)

    if search_query:
        hostel_results = Hostel.objects.filter(
            Q(name__icontains=search_query) | Q(
                location__icontains=search_query)
        )

    else:
        hostel_results = Hostel.objects.all()

    filter_params = request.query_params.dict()
    filter_params.pop('q', None)
    if filter_params:
        hostel_results = HostelFilter(
            filter_params, queryset=hostel_results).qs

    hostel_serializer = HostelSerializer(hostel_results, many=True)
    return Response({'hostelResults': hostel_serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def search_rooms(request):
    filter_params = request.query_params.dict()
    q = filter_params.pop('q', None)

    if q:
        room_results = Room.objects.filter(
            Q(hostel__name__icontains=q) |
            Q(bedspace__icontains=q) |
            Q(sex__icontains=q) |
            Q(description__icontains=q) |
            Q(hostel__location__icontains=q)
        )
    else:
        room_results = Room.objects.all()

    # Apply filtering to search results
    if filter_params:
        room_results = RoomFilter(filter_params, queryset=room_results).qs

    room_serializer = RoomSerializer(room_results, many=True, context={'request': request})

    return Response({'roomResults': room_serializer.data}, status=status.HTTP_200_OK)


# ------------------ FILTER VIEWS -----------------------
@api_view(['GET'])
@permission_classes([AllowAny])
def filter_hostels(request):
    hostels = Hostel.objects.all()
    hostel_filter = HostelFilter(request.GET, queryset=hostels)
    serializer = HostelSerializer(hostel_filter.qs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def filter_rooms(request):
    rooms = Room.objects.all()
    hostel_filter = RoomFilter(request.GET, queryset=rooms)
    serializer = RoomSerializer(hostel_filter.qs, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


# ------------------ HOSTEL CRUD VIEWS -----------------------
@api_view(['GET'])
@permission_classes([AllowAny])
def hostel_list(request):
    hostels = Hostel.objects.all()
    serializer = HostelSerializer(hostels, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def hostel_detail(request, hostel_id):
    try:
        hostel = Hostel.objects.get(id=hostel_id)
    except Hostel.DoesNotExist:
        return Response({'message': 'Hostel not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = HostelSerializer(hostel)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_hostel(request):
    serializer = HostelSerializer(data=request.data)
    print("request.data: ", request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def delete_hostel(request, hostel_id):
    try:
        hostel = Hostel.objects.get(id=hostel_id)
    except Hostel.DoesNotExist:
        return Response({'message': 'Hostel not found'}, status=status.HTTP_404_NOT_FOUND)

    hostel.delete()
    return Response({'message': 'Hostel deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# ----------------- ROOM CRUD VIEWS ---------------------------------
@api_view(['GET'])
def rooms_list_all(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def room_list(request, hostel_id):
    try:
        rooms = Room.objects.filter(hostel__id=hostel_id)
    except Room.DoesNotExist:
        return Response({'message': 'Rooms not found'}, status=status.HTTP_404_NOT_FOUND)

    # Pass the request object as part of the context when instantiating the serializer
    serializer = RoomSerializer(rooms, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def room_list_by_id(request, room_id):
    try:
        rooms = Room.objects.filter(id=room_id)
    except Room.DoesNotExist:
        return Response({'message': 'Rooms not found'}, status=status.HTTP_404_NOT_FOUND)

    # Pass the request object as part of the context when instantiating the serializer
    serializer = RoomSerializer(rooms, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def room_detail(request, hostel_id, room_id):
    try:
        room = Room.objects.get(hostel__id=hostel_id, room_id=room_id)
    except Room.DoesNotExist:
        return Response({'message': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)

    # Pass the request object as part of the context when instantiating the serializer
    serializer = RoomSerializer(room, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_room(request, hostel_id):
    try:
        hostel = Hostel.objects.get(id=hostel_id)
    except Hostel.DoesNotExist:
        return Response({'message': 'Hostel not found'}, status=status.HTTP_404_NOT_FOUND)
    request.data['hostel'] = hostel.id

    serializer = RoomSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_room(request, hostel_id, room_id):
    try:
        room = Room.objects.get(hostel__id=hostel_id, room_id=room_id)
    except Room.DoesNotExist:
        return Response({'message': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = RoomSerializer(room, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_room(request, hostel_id, room_id):
    try:
        room = Room.objects.get(hostel__id=hostel_id, room_id=room_id)
    except Room.DoesNotExist:
        return Response({'message': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)

    room.delete()
    return Response({'message': 'Room deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
