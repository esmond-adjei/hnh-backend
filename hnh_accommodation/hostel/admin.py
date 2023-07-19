from django.contrib import admin
from .models import Hostel, Room
# Register your models here.


class HostelPanel(admin.ModelAdmin):
    list_display = ('name', 'location', 'rating', 'available_rooms')


class RoomPanel(admin.ModelAdmin):
    list_display = ('hostel', 'room_id', 'price',
                    'bedspace', 'number_available')


admin.site.register(Hostel, HostelPanel)
admin.site.register(Room, RoomPanel)
