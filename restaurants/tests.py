import datetime
from django.test import TestCase
from rest_framework.test import APITestCase
from restaurants.models import Restaurant
from django.urls import reverse
from django.contrib.auth import get_user_model


class TestRestaurantModel(TestCase):
    def setUp(self):
        self.restaurant_info = {
            "name": "Test Restaurant",
            "description": "Test Description",
            "address": "Test Address",
            "contact": "Test Contact",
            "open_time": datetime.time(10, 0, 0),
            "close_time": datetime.time(22, 0, 0),
            "last_order": datetime.time(21, 0, 0),
            "regular_holiday": "MON",
        }

    def test_create_restaurant(self):
        restaurant = Restaurant.objects.create(**self.restaurant_info)

        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertEqual(restaurant.name, self.restaurant_info["name"])
        self.assertEqual(restaurant.description, self.restaurant_info["description"])
        self.assertEqual(restaurant.address, self.restaurant_info["address"])
        self.assertEqual(restaurant.contact, self.restaurant_info["contact"])
        self.assertEqual(restaurant.open_time, self.restaurant_info["open_time"])
        self.assertEqual(restaurant.close_time, self.restaurant_info["close_time"])
        self.assertEqual(restaurant.last_order, self.restaurant_info["last_order"])
        self.assertEqual(restaurant.regular_holiday, self.restaurant_info["regular_holiday"])
        self.assertEqual(str(restaurant), self.restaurant_info["name"])


class TestRestaurantView(APITestCase):
    def setUp(self):
        # ✅ permission(IsAuthenticatedOrReadOnly) 때문에 로그인 필요
        User = get_user_model()
        self.user = User.objects.create_user(
            email="rest@test.com",
            nickname="restuser",
            password="password1234",
        )
        self.client.login(email="rest@test.com", password="password1234")

        self.restaurant_info = {
            "name": "Test Restaurant",
            "description": "Test Description",
            "address": "Test Address",
            "contact": "Test Contact",
            "open_time": "10:00:00",
            "close_time": "22:00:00",
            "last_order": "21:00:00",
            "regular_holiday": "MON",
        }

    def test_restaurant_list_view(self):
        url = reverse("restaurant-list")
        Restaurant.objects.create(
            name=self.restaurant_info["name"],
            description=self.restaurant_info["description"],
            address=self.restaurant_info["address"],
            contact=self.restaurant_info["contact"],
            open_time=datetime.time(10, 0, 0),
            close_time=datetime.time(22, 0, 0),
            last_order=datetime.time(21, 0, 0),
            regular_holiday=self.restaurant_info["regular_holiday"],
        )

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        data = response.data
        results = data["results"] if isinstance(data, dict) else data

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], self.restaurant_info["name"])

    def test_restaurant_post_view(self):
        url = reverse("restaurant-list")
        response = self.client.post(url, self.restaurant_info, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertEqual(Restaurant.objects.first().name, self.restaurant_info["name"])

    def test_restaurant_detail_view(self):
        restaurant = Restaurant.objects.create(
            name=self.restaurant_info["name"],
            description=self.restaurant_info["description"],
            address=self.restaurant_info["address"],
            contact=self.restaurant_info["contact"],
        )
        url = reverse("restaurant-detail", kwargs={"pk": restaurant.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], self.restaurant_info["name"])

    def test_restaurant_update_view(self):
        restaurant = Restaurant.objects.create(
            name=self.restaurant_info["name"],
            description=self.restaurant_info["description"],
            address=self.restaurant_info["address"],
            contact=self.restaurant_info["contact"],
        )
        url = reverse("restaurant-detail", kwargs={"pk": restaurant.id})

        updated_restaurant_info = {
            "name": "Updated Restaurant",
            "description": "Updated Description",
            "address": "Updated Address",
            "contact": "Updated Contact",
            "open_time": "11:00:00",
            "close_time": "23:00:00",
            "last_order": "22:00:00",
            "regular_holiday": "TUE",
        }

        response = self.client.put(url, updated_restaurant_info, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], updated_restaurant_info["name"])

    def test_restaurant_delete_view(self):
        restaurant = Restaurant.objects.create(
            name=self.restaurant_info["name"],
            description=self.restaurant_info["description"],
            address=self.restaurant_info["address"],
            contact=self.restaurant_info["contact"],
        )
        url = reverse("restaurant-detail", kwargs={"pk": restaurant.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Restaurant.objects.count(), 0)
