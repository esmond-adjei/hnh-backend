from rest_framework import serializers
from .models import Hostel, Room, Amenity
# , Gallery


class HostelSerializer(serializers.ModelSerializer):
    manager_username = serializers.SerializerMethodField()
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

    def get_manager_username(self, obj):
        if obj.manager:
            return obj.manager.username
        else:
            return 'unknown'


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = '__all__'


# class GallerySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Gallery
#         fields = ('image_url',)



class RoomSerializer(serializers.ModelSerializer):
    amenities = AmenitySerializer(many=True)
    hostel = serializers.StringRelatedField()
    is_collected = serializers.SerializerMethodField()
    # gallery = GallerySerializer(many=True, required=False)

    class Meta:
        model = Room
        fields = '__all__'

    def get_is_collected(self, obj):
        user = self.context.get('request').user

        print(f"==== COLLECTED FOR USER === {user}") # THE REQUEST PASSED DOES NOT HAVE THE USERS INFO APPENDED

        if user.is_authenticated and user.collections.filter(rooms=obj).exists():
            return True

        return False
    
    # def create(self, validated_data):
    #     gallery_data = validated_data.pop('gallery', [])
    #     room = Room.objects.create(**validated_data)
    #     for gallery_item in gallery_data:
    #         Gallery.objects.create(room=room, **gallery_item)
    #     return room