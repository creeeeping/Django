from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Todo, Comment


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = [
            "title",
            "description",
            "start_date",
            "end_date",
            "is_completed",
            "completed_image",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": SummernoteWidget(),
            "start_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "end_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "is_completed": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "completed_image": forms.FileInput(attrs={"class": "form-control"}),
        }



class TodoUpdateForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["title", "description", "start_date", "end_date", "is_completed", "completed_image"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": SummernoteWidget(), 
            "start_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "end_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "is_completed": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "completed_image": forms.FileInput(attrs={"class": "form-control"}),  # ✅ 이미지 첨부칸
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 3, "placeholder": "댓글을 입력하세요", "style": "width:100%;"}),
        }
