from rest_framework import serializers
from .models import Hostel, Room, Facility


class HostelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hostel
        fields = '__all__'

    # This is optional
    def validate_rating(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError(
                "Rating must be between 0 and 5.")
        return value

    # Optional: Customize the representation of a single object (if needed)
    def to_representation(self, instance):
        if instance.available_rooms == 0:
            available_rooms_representation = "Fully Booked"
        else:
            available_rooms_representation = f"{instance.available_rooms} rooms available"

        data = super().to_representation(instance)
        data['available_rooms'] = available_rooms_representation
        return data


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    facilities = FacilitySerializer(many=True)
    hostel = serializers.StringRelatedField()

    class Meta:
        model = Room
        fields = '__all__'
