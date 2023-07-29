from django.contrib import admin
from .models import HUser, HManager, HGuest


class ManagerPanel(admin.ModelAdmin):
    list_display = ('username', 'email', 'get_managed_hostels')

    def get_managed_hostels(self, obj):
        return ', '.join([hostel.name for hostel in obj.hostels_managed.all()])

    get_managed_hostels.short_description = 'Managed Hostels'


admin.site.register(HUser)
admin.site.register(HManager, ManagerPanel)
admin.site.register(HGuest)
