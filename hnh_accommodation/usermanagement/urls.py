from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import register, login, user_collections, add_to_collection, remove_from_collection
from .views_auth import MyTokenObtainPairView

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('collections/<str:user_id>/', user_collections, name='user_collections'),
    path('collections/<str:user_id>/add/', add_to_collection, name='add_to_collection'),
    path('collections/<str:user_id>/remove/', remove_from_collection, name='remove_from_collection'),
]