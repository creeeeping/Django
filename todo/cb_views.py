from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Todo, Comment
from .forms import CommentForm, TodoForm, TodoUpdateForm


class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    template_name = "todo/todo_list.html"
    paginate_by = 5

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
        context["comments"] = Comment.objects.filter(todo=self.object).select_related("user").order_by("-created_at")
        return context


class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    template_name = "todo/todo_create.html"
    form_class = TodoForm

    def form_valid(self, form):
        todo = form.save(commit=False)
        todo.user = self.request.user
        todo.save()
        self.object = todo
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("cbv_todo_info", kwargs={"pk": self.object.pk})


class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    template_name = "todo/todo_update.html"
    form_class = TodoUpdateForm

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user and not self.request.user.is_staff:
            raise Http404("권한 없음")
        return obj

    def get_success_url(self):
        return reverse_lazy("cbv_todo_info", kwargs={"pk": self.object.pk})


class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo
    success_url = reverse_lazy("cbv_todo_list")


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.todo_id = self.kwargs["pk"] 
        comment.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("cbv_todo_info", kwargs={"pk": self.kwargs["pk"]})


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "todo/comment_update.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise Http404("수정 권한 없음")
        return obj

    def get_success_url(self):
        return reverse_lazy("cbv_todo_info", kwargs={"pk": self.object.todo_id})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "todo/comment_confirm_delete.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise Http404("삭제 권한 없음")
        return obj

    def get_success_url(self):
        return reverse_lazy("cbv_todo_info", kwargs={"pk": self.object.todo_id})
