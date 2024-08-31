from django.contrib import admin
from .models import Hostel, Room, Amenity

class CustomAdminSite(admin.AdminSite):
    site_header = 'Campus Hostels Finder'
    site_title = 'Campus Hostels Finder Admin Panel'
    index_title = 'Welcome to Campus Hostels Finder Admin Panel'

admin_site = CustomAdminSite(name='chfadmin')

class HostelPanel(admin.ModelAdmin):
    list_display = ('name', 'location', 'rating', 'available_rooms')


class RoomPanel(admin.ModelAdmin):
    list_display = ('hostel', 'room_id', 'price',
                    'bedspace', 'number_available')


admin_site.register(Hostel, HostelPanel)
admin_site.register(Room, RoomPanel)
admin_site.register(Amenity)
