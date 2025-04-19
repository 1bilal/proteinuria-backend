from rest_framework import serializers
from django.contrib.auth.models import User
from .models import TestResult


class TestResultSerializer(serializers.ModelSerializer):
    result = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = TestResult
        fields = '__all__'
        read_only_fields = ['user']

    def validate(self, data):
        print("Incoming data:", data)
        
        entry_method = data.get('entry_method')
        result = data.get('result')

        print("entry_method:", entry_method)
        print("result:", result)

        if entry_method == TestResult.USER_INPUT and not result:
            raise serializers.ValidationError({
                'result': 'This field is required for manual entries.'
            })

        if entry_method == TestResult.AUTO_DETECTED and not result:
            data['result'] = 'Pending Detection'

        return data



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']