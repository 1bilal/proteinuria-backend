from django.urls import path

from .views import (
    CustomObtainAuthToken,
    ProfileView,
    SignupView,
    UserUpdateView,
)

urlpatterns = [
    path("token/", CustomObtainAuthToken.as_view(), name="custom_login"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("user_update/", UserUpdateView.as_view(), name="user_update"),
]
