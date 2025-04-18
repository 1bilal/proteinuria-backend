from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import TestResult
from .serializers import TestResultSerializer, UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


class TestResultViewSet(viewsets.ModelViewSet):
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        entry_method = self.request.data.get('entry_method', 'manual')
        if entry_method == 'auto':
            serializer.save(user=self.request.user, entry_method='auto')
        else:
            serializer.save(user=self.request.user, entry_method=entry_method)
    
    def get_queryset(self):
        return TestResult.objects.filter(user=self.request.user)

# User Info API
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_info(request):
    serializer = UserSerializer(request.user)
    print(serializer.data)
    return Response(serializer.data)