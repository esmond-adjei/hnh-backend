from django.urls import path
from . import views

urlpatterns = [
    path('hostels/', views.hostel_list, name='hostel-list'),
    path('hostels/<uuid:hostel_id>/', views.hostel_detail, name='hostel-detail'),
    path('hostels/create/', views.create_hostel, name='create-hostel'),
    path('hostels/<uuid:hostel_id>/update/',
         views.update_hostel, name='update-hostel'),
    path('hostels/<uuid:hostel_id>/delete/',
         views.delete_hostel, name='delete-hostel'),
]
