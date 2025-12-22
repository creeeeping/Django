from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('제목', max_length=50)
    description = models.TextField('설명')
    start_date = models.DateField('시작일')
    end_date = models.DateField('마감일')
    is_completed = models.BooleanField('완료 여부', default=False)
    created_at = models.DateTimeField('생성일', auto_now_add=True)
    modified_at = models.DateTimeField('수정일', auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class Comment(models.Model):
    todo = models.ForeignKey(
        Todo,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    message = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.message[:20]}"
