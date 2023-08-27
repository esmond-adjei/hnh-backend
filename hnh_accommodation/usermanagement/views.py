
from .models import HGuest, Collection
from hostel.models import Room
from .serializers import CollectionSerializer
from .serializers import UserSerializer
from .views_auth import MyTokenObtainPairView

from django.contrib.auth import authenticate, login as django_login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status



@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        django_login(request, user)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        response_data = {
            "refresh": str(refresh),
            "access": access_token,
            "user_id": str(user.id),
            "username": user.username,
            "email": user.email,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)

    if user is not None:
        django_login(request, user)
        return MyTokenObtainPairView.as_view()(request._request)
    else:
        return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)


# ------------------ USER COLLECTIONS CRUD VIEWS -----------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated]) # handled authenticated user
def user_collections(request, user_id):
    user_collections = Collection.objects.filter(user=user_id)
    print(f"_________User collections: ", user_collections)
    if user_collections is None:
        return Response({'message': 'User has no collections'}, status=status.HTTP_404_NOT_FOUND)
    serializer = CollectionSerializer(user_collections, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_collection(request, user_id):
    try:
        user = HGuest.objects.get(id=user_id)
    except HGuest.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if 'room_id' not in request.data:
        return Response({'message': 'room_id field is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        room = Room.objects.get(room_id=request.data.get('room_id'))
    except Room.DoesNotExist:
        return Response({'message': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)

    collection, _ = Collection.objects.create(user=user)
    collection.rooms.add(room)

    return Response({'message': 'Room added to collection successfully'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_from_collection(request, user_id):
    print(f"Request data: {request.data}")
    print(f"User id: {user_id}")
    try:
        user = HGuest.objects.get(id=user_id)
    except HGuest.DoesNotExist:
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
