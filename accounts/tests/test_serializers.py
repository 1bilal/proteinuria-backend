from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.serializers import RegisterSerializer, UserSerializer

User = get_user_model()


class RegisterSerializerTest(TestCase):
    def test_valid_registration(self):
        data = {
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "StrongPassword123!",
            "confirm_password": "StrongPassword123!",
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, "test@example.com")

    def test_password_mismatch(self):
        data = {
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "StrongPassword123!",
            "confirm_password": "differentpassword",
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)

    def test_missing_required_fields(self):
        data = {
            "email": "test@example.com",
            "password": "StrongPassword123!",
            "confirm_password": "StrongPassword123!",
        }  # Missing first_name and last_name
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("first_name", serializer.errors)
        self.assertIn("last_name", serializer.errors)


class UserSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com",
            password="StrongPassword123!",
            first_name="Test",
            last_name="User",
        )

    def test_user_serialization(self):
        serializer = UserSerializer(instance=self.user)
        expected_data = {
            "id": self.user.id,
            "email": "user@example.com",
            "first_name": "Test",
            "last_name": "User",
            "state": None,
            "lga": None,
            "dob": None,
            "sex": None,
            "phone_number": None,
        }
        # We don't expect password in the serialized output for GET requests
        serialized_data = serializer.data
        self.assertNotIn("password", serialized_data)
        # Compare other fields
        for key, value in expected_data.items():
            self.assertEqual(serialized_data[key], value)

    def test_user_update(self):
        update_data = {
            "first_name": "Updated",
            "phone_number": "1234567890",
            "password": "newpassword",
        }
        serializer = UserSerializer(instance=self.user, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()

        self.assertEqual(updated_user.first_name, "Updated")
        self.assertEqual(updated_user.phone_number, "1234567890")
        self.assertTrue(updated_user.check_password("newpassword"))

    def test_user_update_invalid_email(self):
        update_data = {"email": "invalid-email"}
        serializer = UserSerializer(instance=self.user, data=update_data, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
