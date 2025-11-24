from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import TestResult
from .serializers import TestResultSerializer
from .utils.color_detection import detect_color

User = get_user_model()


class TestResultViewSet(viewsets.ModelViewSet):
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        image = self.request.FILES.get("image")

        if image:  # If an image is present, it's an auto-detection
            result = detect_color(image)
            serializer.save(user=self.request.user, entry_method="auto", result=result)
        else:  # No image means it's a manual entry
            # The serializer's `validate` method ensures `result` is present for manual entries
            serializer.save(user=self.request.user, entry_method="manual")

    def get_queryset(self):
        return TestResult.objects.filter(user=self.request.user)
