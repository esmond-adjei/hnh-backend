from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Hostel, Room
from .serializers import HostelSerializer, RoomSerializer
from .filters import HostelFilter, RoomFilter
from django.db.models import Q


# SEARCH VIEWS
@api_view(['GET'])
def search(request):
    search_query = request.query_params.get('q', None)

    if search_query:
        # Perform a generalized search using Q objects on relevant fields
        hostel_results = Hostel.objects.filter(
            Q(name__icontains=search_query) | Q(
                location__icontains=search_query)
        )
        # room_results = Room.objects.filter(
        #     Q(hostel__name__icontains=search_query) |
        #     Q(bedspace__icontains=search_query) |
        #     Q(description__icontains=search_query)
        # )
    else:
        hostel_results = Hostel.objects.none()
        # room_results = Room.objects.none()

    # Apply filtering to search results
    filter_params = request.query_params.dict()
    filter_params.pop('q', None)
    if filter_params:
        hostel_results = HostelFilter(
            filter_params, queryset=hostel_results).qs
        # room_results = RoomFilter(filter_params, queryset=room_results).qs

    hostel_serializer = HostelSerializer(hostel_results, many=True)
    # room_serializer = RoomSerializer(room_results, many=True)

    # print(f"hostelResults: {hostel_serializer.data}")
    return Response({
        'hostelResults': hostel_serializer.data,
        # 'room-results': room_serializer.data,
    }, status=status.HTTP_200_OK)


# FILTER VIEWS
@api_view(['GET'])
def filter_hostels(request):
    hostels = Hostel.objects.all()
    hostel_filter = HostelFilter(request.GET, queryset=hostels)
    serializer = HostelSerializer(hostel_filter.qs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def filter_rooms(request):
    rooms = Room.objects.all()
    hostel_filter = RoomFilter(request.GET, queryset=rooms)
    serializer = RoomSerializer(hostel_filter.qs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


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
    print("request.data: ", request.data)
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


# Room views
@api_view(['GET'])
def room_list(request, hostel_id):
    try:
        rooms = Room.objects.filter(hostel__id=hostel_id)
    except Room.DoesNotExist:
        return Response({'message': 'Rooms not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def room_detail(request, hostel_id, room_id):
    try:
        room = Room.objects.get(hostel__id=hostel_id, room_id=room_id)
    except Room.DoesNotExist:
        return Response({'message': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = RoomSerializer(room)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_room(request, hostel_id):
    # Retrieve the hostel based on hostel_id
    try:
        hostel = Hostel.objects.get(id=hostel_id)
    except Hostel.DoesNotExist:
        return Response({'message': 'Hostel not found'}, status=status.HTTP_404_NOT_FOUND)

    # Assign the hostel to the room
    request.data['hostel'] = hostel.id

    serializer = RoomSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
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
def delete_room(request, hostel_id, room_id):
    try:
        room = Room.objects.get(hostel__id=hostel_id, room_id=room_id)
    except Room.DoesNotExist:
        return Response({'message': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)

    room.delete()
    return Response({'message': 'Room deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
