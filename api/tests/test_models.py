import io

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from PIL import Image

from api.models import TestResult

User = get_user_model()


class TestResultModelTest(TestCase):
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

    def test_create_manual_test_result(self):
        result = TestResult.objects.create(
            user=self.user,
            result="Negative",
            entry_method=TestResult.USER_INPUT,
            notes="Feeling good",
        )
        self.assertEqual(result.user, self.user)
        self.assertEqual(result.result, "Negative")
        self.assertEqual(result.entry_method, TestResult.USER_INPUT)
        self.assertEqual(result.notes, "Feeling good")
        self.assertIsNotNone(result.timestamp)
        self.assertIsNotNone(result.created_at)
        self.assertIsNone(result.image.name)

    def test_create_auto_detected_test_result(self):
        image_file = self.create_image()
        result = TestResult.objects.create(
            user=self.user,
            result="Trace",
            image=image_file,
            entry_method=TestResult.AUTO_DETECTED,
        )
        self.assertEqual(result.user, self.user)
        self.assertEqual(result.result, "Trace")
        self.assertEqual(result.entry_method, TestResult.AUTO_DETECTED)
        self.assertIsNotNone(result.image.name)

    def test_test_result_str_representation(self):
        result = TestResult.objects.create(
            user=self.user, result="+1", entry_method=TestResult.USER_INPUT
        )
        self.assertEqual(
            str(result), f"{result.result} ({result.entry_method}) - {result.timestamp}"
        )
