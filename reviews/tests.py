from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from restaurants.models import Restaurant
from reviews.models import Review

User = get_user_model()


# =========================
# Review Model Test (기존 유지)
# =========================
class TestReviewModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            nickname="testuser",
            email="test@example.com",
            password="password1234",
        )
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            description="Test Description",
            address="123 Test St",
            contact="Phone: 010-0000-0000",
        )
        self.data = {
            "user": self.user,
            "restaurant": self.restaurant,
            "title": "Test Review Title",
            "comment": "Tasty Yammy Yammy~",
        }

    def test_create_review(self):
        review = Review.objects.create(**self.data)

        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(review.title, self.data["title"])
        self.assertEqual(review.comment, self.data["comment"])
        self.assertEqual(review.user, self.data["user"])
        self.assertEqual(review.restaurant, self.data["restaurant"])


# =========================
# Review APIView / GenericView Test (추가)
# =========================
class TestReviewAPIView(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="review@test.com",
            nickname="reviewuser",
            password="password1234",
        )
        self.client.login(email="review@test.com", password="password1234")

        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            description="Test Description",
            address="Test Address",
            contact="010-0000-0000",
        )

    def test_get_review_list(self):
        Review.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            title="Test Title",
            comment="Test Comment",
        )

        url = reverse("review-list", kwargs={"restaurant_id": self.restaurant.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        data = response.data
        results = data["results"] if isinstance(data, dict) else data
        self.assertEqual(len(results), 1)

    def test_post_review(self):
        url = reverse("review-list", kwargs={"restaurant_id": self.restaurant.id})
        response = self.client.post(
            url,
            {"title": "New Review", "comment": "So good!"},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Review.objects.count(), 1)

    def test_get_review_detail(self):
        review = Review.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            title="Detail Title",
            comment="Detail Comment",
        )

        url = reverse("review-detail", kwargs={"review_id": review.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_update_review(self):
        review = Review.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            title="Old Title",
            comment="Old Comment",
        )

        url = reverse("review-detail", kwargs={"review_id": review.id})
        response = self.client.patch(
            url,
            {"title": "Updated Title"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)

    def test_delete_review(self):
        review = Review.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            title="Delete Title",
            comment="Delete Comment",
        )

        url = reverse("review-detail", kwargs={"review_id": review.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
