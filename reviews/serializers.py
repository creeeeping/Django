from rest_framework import serializers
from reviews.models import Review
from users.serializers import UserDetailSerializer
from restaurants.serializers import RestaurantSerializer


class ReviewSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Review
        fields = (
            "id",
            "user",
            "title",
            "comment",
        )
        read_only_fields = ("id",)


class ReviewDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    restaurant = RestaurantSerializer(read_only=True)

    class Meta:
        model = Review
        fields = (
            "id",
            "user",
            "restaurant",
            "title",
            "comment",
        )
        read_only_fields = ("id",)
