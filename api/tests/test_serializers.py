import io

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from PIL import Image

from api.models import TestResult
from api.serializers import TestResultSerializer

User = get_user_model()


class TestResultSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="StrongPassword123!",
            first_name="John",
            last_name="Doe",
        )

    def create_image(
        self, name="test_image.jpg", size=(100, 100), color=(255, 255, 255)
    ):
        file_obj = io.BytesIO()
        image = Image.new("RGB", size, color)
        image.save(file_obj, "jpeg")
        file_obj.seek(0)
        return SimpleUploadedFile(name, file_obj.read(), content_type="image/jpeg")

    def test_manual_entry_serializer_valid(self):
        data = {
            "user": self.user.id,
            "result": "Negative",
            "entry_method": TestResult.USER_INPUT,
            "notes": "Manual entry test",
        }
        serializer = TestResultSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        test_result = serializer.save(user=self.user)
        self.assertEqual(test_result.result, "Negative")
        self.assertEqual(test_result.entry_method, TestResult.USER_INPUT)

    def test_manual_entry_serializer_missing_result(self):
        data = {
            "user": self.user.id,
            "entry_method": TestResult.USER_INPUT,
            "notes": "Manual entry test",
        }
        serializer = TestResultSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("result", serializer.errors)

    def test_auto_detected_serializer_valid_with_result(self):
        image_file = self.create_image()
        data = {
            "user": self.user.id,
            "result": "+1",
            "entry_method": TestResult.AUTO_DETECTED,
            "image": image_file,
        }
        serializer = TestResultSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        test_result = serializer.save(user=self.user)
        self.assertEqual(test_result.result, "+1")
        self.assertEqual(test_result.entry_method, TestResult.AUTO_DETECTED)
        self.assertIsNotNone(test_result.image)

    def test_auto_detected_serializer_no_result_provided(self):
        image_file = self.create_image()
        data = {
            "user": self.user.id,
            "entry_method": TestResult.AUTO_DETECTED,
            "image": image_file,
        }
        serializer = TestResultSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        test_result = serializer.save(user=self.user)
        self.assertEqual(test_result.result, "Pending Detection")
        self.assertEqual(test_result.entry_method, TestResult.AUTO_DETECTED)
        self.assertIsNotNone(test_result.image)
