from django.urls import path
from . import views

urlpatterns = [
    path('', views.search, name='search-hostels'),
    path('hostels/', views.filter_hostels, name='filter-hostels'),
    path('rooms/', views.filter_rooms, name='filter-rooms'),
]
