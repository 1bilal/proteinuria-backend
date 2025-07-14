from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email="test@example.com",
            password="StrongPassword123!",
            first_name="John",
            last_name="Doe",
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("StrongPassword123!"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")

    def test_create_user_without_email(self):
        with self.assertRaisesMessage(ValueError, "The Email field must be set"):
            User.objects.create_user(
                email=None,
                password="StrongPassword123!",
                first_name="John",
                last_name="Doe",
            )

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            email="admin@example.com",
            password="StrongPassword123!",
            first_name="Admin",
            last_name="User",
        )
        self.assertEqual(admin_user.email, "admin@example.com")
        self.assertTrue(admin_user.check_password("StrongPassword123!"))
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_active)

    def test_create_superuser_without_password(self):
        with self.assertRaisesMessage(ValueError, "Superusers must have a password."):
            User.objects.create_superuser(
                email="admin@example.com",
                password=None,
                first_name="Admin",
                last_name="User",
            )

    def test_email_unique(self):
        User.objects.create_user(
            email="unique@example.com",
            password="StrongPassword123!",
            first_name="Test",
            last_name="User",
        )
        with self.assertRaises(Exception):  # IntegrityError or ValidationError
            User.objects.create_user(
                email="unique@example.com",
                password="StrongPassword123!",
                first_name="Another",
                last_name="User",
            )

    def test_user_str_representation(self):
        user = User.objects.create_user(
            email="strtest@example.com",
            password="StrongPassword123!",
            first_name="Test",
            last_name="User",
        )
        self.assertEqual(str(user), "strtest@example.com")
