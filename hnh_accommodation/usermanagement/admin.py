from django.contrib import admin
from .models import HUser, HGuest, HManager


class ManagerPanel(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_verified')


admin.site.register(HUser)
admin.site.register(HManager, ManagerPanel)
