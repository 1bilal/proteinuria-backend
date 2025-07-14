from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TestResultViewSet

router = DefaultRouter()
router.register(r"test-results", TestResultViewSet, basename="test-result")

urlpatterns = router.urls
