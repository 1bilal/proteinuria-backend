from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User

from .models import TestResult
from .serializers import TestResultSerializer, UserSerializer
from .utils.color_detection import detect_color



class TestResultViewSet(viewsets.ModelViewSet):
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        entry_method = self.request.data.get('entry_method', 'manual')
        image = self.request.FILES.get('image')
        result = self.request.data.get('result')

        if entry_method == 'auto' and not result:
            print("Auto mode: Detecting color...")
            result = detect_color(image)
            print("Detected color:", result)

            serializer.save(user=self.request.user, entry_method='auto', result=result) 
        else:
            serializer.save(user=self.request.user, entry_method=entry_method)
    
    def get_queryset(self):
        return TestResult.objects.filter(user=self.request.user)

# User Info API
from rest_framework.authentication import TokenAuthentication

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([TokenAuthentication])  # Add Token Authentication here
def user_info(request):
    serializer = UserSerializer(request.user)
    print(serializer.data)  # Debug: Check the serialized data
    return Response(serializer.data)
