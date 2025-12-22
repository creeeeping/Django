from django.contrib.auth.mixins import LoginRequiredMixin
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

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user and not self.request.user.is_staff:
            raise Http404("권한 없음")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        context["comments"] = self.object.comments.all().order_by("-created_at")
        return context


class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    fields = ["title", "description", "start_date", "end_date"]
    template_name = "todo/todo_create.html"

    def form_valid(self, form):
        todo = form.save(commit=False)
        todo.user = self.request.user
        todo.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("cbv_todo_info", kwargs={"pk": self.object.pk})


class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    fields = ["title", "description", "start_date", "end_date", "is_completed"]
    template_name = "todo/todo_update.html"

    def get_success_url(self):
        return reverse_lazy("cbv_todo_info", kwargs={"pk": self.object.pk})


class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo

    def get_success_url(self):
        return reverse_lazy("cbv_todo_list")


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.todo = Todo.objects.get(pk=self.kwargs["todo_pk"])
        comment.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("cbv_todo_info", kwargs={"pk": self.kwargs["todo_pk"]})


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise Http404("수정 권한 없음")
        return obj

    def get_success_url(self):
        return reverse_lazy("cbv_todo_info", kwargs={"pk": self.object.todo.pk})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise Http404("삭제 권한 없음")
        return obj

    def get_success_url(self):
        return reverse_lazy("cbv_todo_info", kwargs={"pk": self.object.todo.pk})
