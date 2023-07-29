
from .models import HUser, Collection
from hostel.models import Room
from .serializers import CollectionSerializer

from django.contrib.auth import authenticate, login as django_login
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)

    print(f"Request data: {request.data}")
    if serializer.is_valid():
        user = serializer.save()
        response_data = {
            'message': 'User registered successfully',
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Authenticate user
    print(f"- Username: {username}\n- Password: {password}")
    user = authenticate(request, username=username, password=password)

    if user is not None:
        # Login the user
        django_login(request, user)
        serializer = UserSerializer(user)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)


# USER COLLECTIONS
@api_view(['GET'])
def user_collections(request, user_id):
    user_collections = Collection.objects.filter(user=user_id)
    serializer = CollectionSerializer(user_collections, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_to_collection(request, user_id):
    print(f"Request data: {request.data}")
    print(f"User id: {user_id}")
    try:
        user = HUser.objects.get(id=user_id)
    except HUser.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if 'room_id' not in request.data:
        return Response({'message': 'room_id field is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        room = Room.objects.get(room_id=request.data.get('room_id'))
    except Room.DoesNotExist:
        return Response({'message': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)

    collection, _ = Collection.objects.get_or_create(user=user)
    collection.rooms.add(room)

    return Response({'message': 'Room added to collection successfully'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def remove_from_collection(request, user_id):
    print(f"Request data: {request.data}")
    print(f"User id: {user_id}")
    try:
        user = HUser.objects.get(id=user_id)
    except HUser.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if 'room_id' not in request.data:
        return Response({'message': 'room_id field is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        room = Room.objects.get(room_id=request.data.get('room_id'))
    except Room.DoesNotExist:
        return Response({'message': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)

    collection, _ = Collection.objects.get_or_create(user=user)
    collection.rooms.remove(room)

    return Response({'message': 'Room removed from collection successfully'}, status=status.HTTP_200_OK)
