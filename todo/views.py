from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from .models import Todo, Comment
from .forms import CommentForm


class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    paginate_by = 5
    template_name = "todo/todo_list.html"

    def get_queryset(self):
        qs = Todo.objects.all().order_by("-created_at")
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)

        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(title__icontains=q)
        return qs


class TodoDetailView(LoginRequiredMixin, DetailView):
    model = Todo
    template_name = "todo/todo_info.html"
    queryset = Todo.objects.prefetch_related("comments", "comments__user")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user and not self.request.user.is_staff:
            raise Http404("권한이 없습니다.")
        return obj

    def get_context_data(self, **kwargs):
        comments = self.object.comments.order_by("-created_at")
        paginator = Paginator(comments, 5)

        return {
            "todo": self.object,
            "comment_form": CommentForm(),
            "page_obj": paginator.get_page(self.request.GET.get("page")),
        }


class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    fields = ["title", "description", "start_date", "end_date"]
    template_name = "todo/todo_create.html"

    def form_valid(self, form):
        to
