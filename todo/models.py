from django.db import models
from django.contrib.auth import get_user_model

from PIL import Image
from pathlib import Path
from io import BytesIO
from django.core.files.base import ContentFile

User = get_user_model()

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('제목', max_length=50)
    description = models.TextField('설명')
    start_date = models.DateField('시작일')
    end_date = models.DateField('마감일')
    is_completed = models.BooleanField('완료 여부', default=False)

    completed_image = models.ImageField(
        upload_to='todo/completed_images/',
        null=True,
        blank=True
    )
    thumbnail = models.ImageField(
        upload_to='todo/thumbnails/',
        null=True,
        blank=True,
        default='todo/no_image/NO-IMAGE.gif', 
    )

    created_at = models.DateTimeField('생성일', auto_now_add=True)
    modified_at = models.DateTimeField('수정일', auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    def save(self, *args, **kwargs):
        """
        completed_image가 들어오면 thumbnail을 100x100으로 자동 생성.
        - Path로 파일명/확장자 처리
        - Pillow thumbnail()
        - BytesIO + ContentFile로 ImageField 저장
        """
        super().save(*args, **kwargs)

        if not self.completed_image:
            return

        try:
            img = Image.open(self.completed_image)
            img.thumbnail((100, 100))

            image_path = Path(self.completed_image.name)
            ext = image_path.suffix.lower()

            if ext in ['.jpg', '.jpeg']:
                file_type = 'JPEG'
            elif ext == '.png':
                file_type = 'PNG'
            elif ext == '.gif':
                file_type = 'GIF'
            else:
                return

            thumb_name = f"{image_path.stem}_thumbnail{ext}"
            thumb_dir = 'todo/thumbnails/'
            thumb_fullname = f"{thumb_dir}{thumb_name}"

            temp = BytesIO()
            img.save(temp, format=file_type)
            temp.seek(0)

            self.thumbnail.save(thumb_fullname, ContentFile(temp.read()), save=False)
            temp.close()

            super().save(update_fields=['thumbnail'])
        except Exception:
            return

class Comment(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:20]