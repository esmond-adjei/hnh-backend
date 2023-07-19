from django.contrib.auth import authenticate, login as django_login
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)  # -xxx

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
