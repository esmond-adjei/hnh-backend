from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import HManager, HGuest, Collection
from hostel.serializers import RoomSerializer
# from hostel.models import Room


User = get_user_model()  # xxx


class HManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HManager
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class HGuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = HGuest
        fields = ['id', 'username', 'email', 'password', 'check_in_date', 'check_out_date',
                  'emergency_contact_name', 'emergency_contact_phone', 'special_requests']
        extra_kwargs = {'password': {'write_only': True}}


def create_user_serializer(user_type):
    """
    Return the appropriate serializer based on the user type.
    """
    if user_type == 'manager':
        return HManagerSerializer
    elif user_type == 'guest':
        return HGuestSerializer
    else:
        raise ValueError('Invalid user type')


class UserSerializer(serializers.ModelSerializer):
    user_type = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'user_type']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user_type = validated_data.pop('user_type')
        serializer_class = create_user_serializer(user_type)
        serializer = serializer_class(data=validated_data)

        if serializer.is_valid():
            user = serializer.save()
            user.set_password(validated_data['password'])
            user.save()
            return user
        else:
            raise serializers.ValidationError(serializer.errors)



class CollectionSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True, read_only=True, context={'request': 'request'})

    class Meta:
        model = Collection
        fields = ['id', 'name', 'user', 'rooms']
