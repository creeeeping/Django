import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='todo',
            options={'verbose_name': '할 일', 'verbose_name_plural': '할 일 목록'},
        ),
        migrations.AddField(
            model_name='todo',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='작성자'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='todo',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='생성일'),
        ),
        migrations.AlterField(
            model_name='todo',
            name='description',
            field=models.TextField(blank=True, verbose_name='설명'),
        ),
        migrations.AlterField(
            model_name='todo',
            name='end_date',
            field=models.DateField(verbose_name='마감일'),
        ),
        migrations.AlterField(
            model_name='todo',
            name='is_completed',
            field=models.BooleanField(default=False, verbose_name='완료 여부'),
        ),
        migrations.AlterField(
            model_name='todo',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='수정일'),
        ),
        migrations.AlterField(
            model_name='todo',
            name='start_date',
            field=models.DateField(verbose_name='시작일'),
        ),
        migrations.AlterField(
            model_name='todo',
            name='title',
            field=models.CharField(max_length=50, verbose_name='제목'),
        ),
    ]
