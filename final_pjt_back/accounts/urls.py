# accounts/urls.py
from django.urls import path
from .views import UserProfileView, CustomUserDetailsView, UserRecommendationsAPIView
from dj_rest_auth.registration.views import RegisterView
from .serializers import CustomRegisterSerializer
from . import views

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/update/', views.modify),   
    path('profile/recommendations/', UserRecommendationsAPIView.as_view(), name='user-recommendations')
]

