from django.db import models
from config.models import BaseModel

DAYS_OF_WEEK = [
    ("MON", "월요일"),
    ("TUE", "화요일"),
    ("WED", "수요일"),
    ("THU", "목요일"),
    ("FRI", "금요일"),
    ("SAT", "토요일"),
    ("SUN", "일요일"),
]


class Restaurant(BaseModel):
    name = models.CharField(
        max_length=50,
        verbose_name="음식점 이름"
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="음식점 설명"
    )
    address = models.CharField(
        max_length=200,
        verbose_name="주소"
    )
    contact = models.CharField(
        max_length=50,
        verbose_name="연락처"
    )
    open_time = models.TimeField(
        null=True,
        blank=True,
        verbose_name="오픈 시간"
    )
    close_time = models.TimeField(
        null=True,
        blank=True,
        verbose_name="마감 시간"
    )
    last_order = models.TimeField(
        null=True,
        blank=True,
        verbose_name="라스트 오더"
    )
    regular_holiday = models.CharField(
        choices=DAYS_OF_WEEK,
        max_length=3,
        null=True,
        blank=True,
        verbose_name="정기 휴무일"
    )

    def __str__(self):
        return self.name


    def __str__(self):
        return self.name
