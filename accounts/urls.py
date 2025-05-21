from django.urls import path
from .views import SignupView, user_info, CustomObtainAuthToken, ProfileView, UserUpdateView


urlpatterns = [
    path('token/', CustomObtainAuthToken.as_view(), name='custom_login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('user/', user_info, name='user_info'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('user_update/', UserUpdateView.as_view(), name='user_update'),
]
