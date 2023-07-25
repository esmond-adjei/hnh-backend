from django.urls import path
from . import views

urlpatterns = [
    path('hostels/', views.search_hostels, name='search-hostels'),
    path('rooms/', views.search_rooms, name='search-rooms'),
    path('hostels/', views.filter_hostels, name='filter-hostels'),
    path('rooms/', views.filter_rooms, name='filter-rooms'),
]
