from django.urls import path
from . import views


urlpatterns = [
    # Hostel views
    path('hostels/', views.hostel_list, name='hostel-list'),
    path('hostel/<uuid:hostel_id>/', views.hostel_detail, name='hostel-detail'),
    path('hostel/create/', views.create_hostel, name='create-hostel'),
    path('hostel/<uuid:hostel_id>/update/',
         views.update_hostel, name='update-hostel'),
    path('hostel/<uuid:hostel_id>/delete/',
         views.delete_hostel, name='delete-hostel'),

    # Room views
    path('rooms/', views.rooms_list_all, name='all-room-list'),
    path('hostel/<uuid:hostel_id>/rooms/', views.room_list, name='room-list'),
    path('hostel/<uuid:hostel_id>/rooms/<int:room_id>/',
         views.room_detail, name='room-detail'),
    path('hostel/<uuid:hostel_id>/rooms/create/',
         views.create_room, name='create-room'),
    path('hostel/<uuid:hostel_id>/rooms/<int:room_id>/update/',
         views.update_room, name='update-room'),
    path('hostel/<uuid:hostel_id>/rooms/<int:room_id>/delete/',
         views.delete_room, name='delete-room'),
]
