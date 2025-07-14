from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

User = get_user_model()


class AccountsViewsTest(APITestCase):
    def setUp(self):
        self.user_data = {
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "StrongPassword123!",
            "confirm_password": "StrongPassword123!",
        }
        self.user = User.objects.create_user(
            email="existing@example.com",
            password="StrongPassword123!",
            first_name="Existing",
            last_name="User",
        )
        self.token = Token.objects.create(user=self.user)

    def test_signup_view(self):
        url = reverse("signup")  # Assuming 'signup' is the name of your signup URL
        response = self.client.post(url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)  # One existing, one new
        self.assertEqual(
            User.objects.get(email="testuser@example.com").first_name, "Test"
        )

    def test_signup_view_password_mismatch(self):
        data = self.user_data.copy()
        data["confirm_password"] = "wrongpassword"
        url = reverse("signup")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_login_view(self):
        url = reverse(
            "custom_login"
        )  # Assuming 'custom_login' is the name of your login URL
        response = self.client.post(
            url,
            {"email": "existing@example.com", "password": "StrongPassword123!"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_login_view_invalid_credentials(self):
        url = reverse("custom_login")
        response = self.client.post(
            url,
            {"email": "existing@example.com", "password": "wrongpassword"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)

    def test_profile_view_get(self):
        url = reverse("profile")  # Assuming 'profile' is the name of your profile URL
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)

    def test_profile_view_update(self):
        url = reverse("profile")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        update_data = {"first_name": "UpdatedFirstName", "phone_number": "1234567890"}
        response = self.client.patch(url, update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "UpdatedFirstName")
        self.assertEqual(self.user.phone_number, "1234567890")

    def test_user_info_view(self):
        url = reverse(
            "user_info"
        )  # Assuming 'user_info' is the name of your user_info URL
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)
