from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


# =========================
# User Model Test
# =========================
class TestUserModel(TestCase):
    def setUp(self):
        self.test_user = {
            "email": "test@example.com",
            "nickname": "testuser",
            "password": "password1234",
        }
        self.test_admin_user = {
            "email": "admin@example.com",
            "nickname": "adminuser",
            "password": "password1234",
        }

    def test_user_manager_create_user(self):
        user = User.objects.create_user(**self.test_user)

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.email, self.test_user["email"])
        self.assertEqual(user.nickname, self.test_user["nickname"])
        self.assertTrue(user.check_password(self.test_user["password"]))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertEqual(user.profile_image.url, "/media/users/blank_profile_image.png")

    def test_user_manager_create_superuser(self):
        admin_user = User.objects.create_superuser(**self.test_admin_user)

        self.assertEqual(User.objects.filter(is_superuser=True, is_staff=True).count(), 1)
        self.assertEqual(admin_user.email, self.test_admin_user["email"])
        self.assertEqual(admin_user.nickname, self.test_admin_user["nickname"])
        self.assertTrue(admin_user.check_password(self.test_admin_user["password"]))
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_active)
        self.assertEqual(admin_user.profile_image.url, "/media/users/blank_profile_image.png")


# =========================
# User APIView / GenericView Test
# =========================
class TestUserAPIView(APITestCase):
    def setUp(self):
        self.signup_url = reverse("user-signup")
        self.login_url = reverse("user-login")

        self.user = User.objects.create_user(
            email="api@test.com",
            nickname="apiuser",
            password="password1234",
        )

    def test_user_signup(self):
        response = self.client.post(
            self.signup_url,
            {
                "email": "new@test.com",
                "nickname": "newuser",
                "password": "password1234",
            },
        )
        self.assertEqual(response.status_code, 201)

    def test_user_login(self):
        response = self.client.post(
            self.login_url,
            {
                "email": "api@test.com",
                "password": "password1234",
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_user_login_invalid_credentials(self):
        response = self.client.post(
            self.login_url,
            {
                "email": "api@test.com",
                "password": "wrongpassword",
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_get_user_details(self):
        self.client.login(email="api@test.com", password="password1234")
        url = reverse("user-detail", kwargs={"pk": self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_user_details(self):
        # ✅ 부분 수정이 목적이므로 PATCH 사용 (PUT은 전체 필드 필요)
        self.client.login(email="api@test.com", password="password1234")
        url = reverse("user-detail", kwargs={"pk": self.user.id})
        response = self.client.patch(url, {"nickname": "updated"}, format="json")
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        self.client.login(email="api@test.com", password="password1234")
        url = reverse("user-detail", kwargs={"pk": self.user.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
