from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TestResultViewSet, user_info

from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'test-results', TestResultViewSet, basename='test-result')

urlpatterns = [
    path('api/token/', obtain_auth_token, name='api_token_auth'),
    path('api/user/', user_info, name='user_info'),
    path('api/', include(router.urls)),
]
