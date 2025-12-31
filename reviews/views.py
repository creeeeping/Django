from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from reviews.models import Review
from restaurants.models import Restaurant
from reviews.serializers import ReviewSerializer, ReviewDetailSerializer


class ReviewListCreateView(ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(
            restaurant_id=self.kwargs["restaurant_id"]
        ).order_by("-id")

    def perform_create(self, serializer):
        restaurant = get_object_or_404(
            Restaurant,
            id=self.kwargs["restaurant_id"]
        )
        serializer.save(
            user=self.request.user,
            restaurant=restaurant
        )


class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(
            Review,
            id=self.kwargs["review_id"],
            user=self.request.user
        )
