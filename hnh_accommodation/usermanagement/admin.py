from django.contrib import admin
from .models import HUser, HManager, HGuest, Collection


class ManagerPanel(admin.ModelAdmin):
    list_display = ('username', 'email', 'get_managed_hostels')

    def get_managed_hostels(self, obj):
        return ', '.join([hostel.name for hostel in obj.hostels_managed.all()])

    get_managed_hostels.short_description = 'Managed Hostels'

class CollectionPanel(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'num_rooms')

    def num_rooms(self, obj):
        return len([room for room in obj.rooms.all()])

    num_rooms.short_description = 'Number of Rooms'


class HUserPanel(admin.ModelAdmin):
    list_display = ('username', 'email')


admin.site.register(HUser, HUserPanel)
admin.site.register(HManager, ManagerPanel)
admin.site.register(HGuest)
admin.site.register(Collection, CollectionPanel)