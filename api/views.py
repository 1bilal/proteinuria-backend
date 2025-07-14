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
        entry_method = self.request.data.get("entry_method", "manual")
        image = self.request.FILES.get("image")
        result = self.request.data.get("result")

        if entry_method == "auto" and not result:
            print("Auto mode: Detecting color...")
            result = detect_color(image)
            print("Detected color:", result)

            serializer.save(user=self.request.user, entry_method="auto", result=result)
        else:
            serializer.save(user=self.request.user, entry_method=entry_method)

    def get_queryset(self):
        return TestResult.objects.filter(user=self.request.user)
