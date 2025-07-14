import io

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from PIL import Image
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from api.models import TestResult

User = get_user_model()


class TestResultViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="StrongPassword123!",
            first_name="Test",
            last_name="User",
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def create_image(
        self, name="test_image.jpg", size=(100, 100), color=(255, 255, 255)
    ):
        file_obj = io.BytesIO()
        image = Image.new("RGB", size, color)
        image.save(file_obj, "jpeg")
        file_obj.seek(0)
        return SimpleUploadedFile(name, file_obj.read(), content_type="image/jpeg")

    def test_create_manual_test_result(self):
        url = reverse(
            "test-result-list"
        )  # Assuming 'test-result-list' is the name for list/create
        data = {
            "result": "Negative",
            "entry_method": TestResult.USER_INPUT,
            "notes": "Manual entry from API test",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TestResult.objects.count(), 1)
        self.assertEqual(TestResult.objects.get().result, "Negative")

    def test_create_auto_detected_test_result_with_image(self):
        url = reverse("test-result-list")
        image_file = self.create_image()
        data = {"entry_method": TestResult.AUTO_DETECTED, "image": image_file}
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TestResult.objects.count(), 1)
        # The result should be 'Pending Detection' or actual detected value
        self.assertIn(
            TestResult.objects.get().result,
            ["Pending Detection", "Negative", "Trace", "+1", "+2", "+3"],
        )
        self.assertIsNotNone(TestResult.objects.get().image)

    def test_list_test_results(self):
        TestResult.objects.create(
            user=self.user, result="Negative", entry_method=TestResult.USER_INPUT
        )
        TestResult.objects.create(
            user=self.user, result="+1", entry_method=TestResult.USER_INPUT
        )
        url = reverse("test-result-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_test_result(self):
        test_result = TestResult.objects.create(
            user=self.user, result="Negative", entry_method=TestResult.USER_INPUT
        )
        url = reverse(
            "test-result-detail", args=[test_result.id]
        )  # Assuming 'test-result-detail' for retrieve/update/delete
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["result"], "Negative")

    def test_update_test_result(self):
        test_result = TestResult.objects.create(
            user=self.user, result="Negative", entry_method=TestResult.USER_INPUT
        )
        url = reverse("test-result-detail", args=[test_result.id])
        update_data = {"result": "+1", "notes": "Updated notes"}
        response = self.client.patch(url, update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_result.refresh_from_db()
        self.assertEqual(test_result.result, "+1")
        self.assertEqual(test_result.notes, "Updated notes")

    def test_delete_test_result(self):
        test_result = TestResult.objects.create(
            user=self.user, result="Negative", entry_method=TestResult.USER_INPUT
        )
        url = reverse("test-result-detail", args=[test_result.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TestResult.objects.count(), 0)
