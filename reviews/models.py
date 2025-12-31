from django.contrib.auth import get_user_model
from django.db import models
from config.models import BaseModel
from restaurants.models import Restaurant

User = get_user_model()

class Review(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="작성자"
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        verbose_name="음식점"
    )
    title = models.CharField(
        max_length=50,
        verbose_name="리뷰 제목"
    )
    comment = models.TextField(
        verbose_name="리뷰 내용"
    )

    def __str__(self):
        return f"{self.restaurant.name} 리뷰"


    def __str__(self):
        return f"{self.restaurant.name} 리뷰"
