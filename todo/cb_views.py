from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import Http404
from .models import Todo

def is_admin(user):
    return user.is_staff or user.is_superuser

class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    template_name = 'todo/todo_list.html'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        qs = Todo.objects.all()
        if not is_admin(self.request.user):
            qs = qs.filter(user=self.request.user)

        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        return qs

class TodoDetailView(LoginRequiredMixin, DetailView):
    model = Todo
    template_name = 'todo/todo_info.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not is_admin(self.request.user) and obj.user != self.request.user:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        return {'todo': self.object}

class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    fields = ['title', 'description', 'start_date', 'end_date']
    template_name = 'todo/todo_create.html'

    def form_valid(self, form):
        todo = form.save(commit=False)
        todo.user = self.request.user
        todo.save()
        self.object = todo
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('cbv_todo_info', kwargs={'pk': self.object.pk})

class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    fields = ['title', 'description', 'start_date', 'end_date', 'is_completed']
    template_name = 'todo/todo_update.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not is_admin(self.request.user) and obj.user != self.request.user:
            raise Http404
        return obj

    def get_success_url(self):
        return reverse_lazy('cbv_todo_info', kwargs={'pk': self.object.pk})

class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not is_admin(self.request.user) and obj.user != self.request.user:
            raise Http404
        return obj

    def get_success_url(self):
        return reverse_lazy('cbv_todo_list')
