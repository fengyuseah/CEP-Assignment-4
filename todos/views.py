from django.shortcuts import render
from .models import Todo
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Q
from todos.forms import TodoForm
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from accounts.models import UserProfile
import json

# Create your views here.
'''
def todos_list(request):
    all_todos = Todo.objects.all()

    return render(request, 'todos/index.html', {'todos' : all_todos})

def todos_detail(request, todo_id):
    todo1 = Todo.objects.get(id=todo_id)
    
    return render(request, 'todos/detail.html', {'todo' : todo1})

def tag_list(request, tag):
    tag_todos = Todo.objects.filter(tag__name__iexact=tag)
    
    return render(request, 'todos/taglist.html', {'todos' : tag_todos, 'tag' : tag})
'''

class TodoList(ListView):
    model = Todo
    
    queryset = Todo.objects.all()
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TodoList, self).dispatch(*args, **kwargs)
    
    def get_queryset(self):
        curruser = UserProfile.objects.get(user=self.request.user)
        todos = Todo.objects.all().filter(user=curruser)
        self.queryset = todos
        return todos
        
    def get_context_data(self, **kwargs):
        context = super(TodoList, self).get_context_data(**kwargs)
        context['curruser'] = UserProfile.objects.get(user=self.request.user)
        return context

class TagList(ListView):
    model = Todo
    
    queryset = Todo.objects.all()
    
    def get_queryset(self):
        curruser = UserProfile.objects.filter(user=self.request.user)
        tagn = self.kwargs['tag']
        #pieces = tags.split('/') #extract different tags separated by /
        
        #queries = [Q(tag__name__iexact=value) for value in pieces]
        # Take one Q object from the list
        #query = queries.pop()
        query = Q(tag__name__iexact=tagn)
        # Or the Q object with the ones remaining in the list
        #for item in queries:
        #query |= item
        # Query the model
        todos = Todo.objects.filter(user=curruser).filter(query).distinct().order_by('tag__name')
        self.queryset = todos #Setting the queryset to allow get_context_data to apply count
        return todos
        
    def get_context_data(self, **kwargs):
        context = super(TagList, self).get_context_data(**kwargs)
        context['tag'] = self.kwargs['tag']
        context['curruser'] = UserProfile.objects.get(user=self.request.user)
        return context
        
class TodoCreate(CreateView):
    model = Todo
    form_class = TodoForm
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TodoCreate, self).dispatch(*args, **kwargs)
        
    def form_valid(self, form):
        curruser = UserProfile.objects.get(user=self.request.user)
        form.instance.user = curruser
        form.save()
        return super(TodoCreate, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(TodoCreate, self).get_context_data(**kwargs)
        context['curruser'] = UserProfile.objects.get(user=self.request.user)
        return context
    
class TodoUpdate(UpdateView):
    model = Todo
    form_class = TodoForm
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TodoUpdate, self).dispatch(*args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super(TodoUpdate, self).get_context_data(**kwargs)
        context['curruser'] = UserProfile.objects.get(user=self.request.user)
        return context

class TodoDetail(DetailView):
    model = Todo
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TodoDetail, self).dispatch(*args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super(TodoDetail, self).get_context_data(**kwargs)
        context['curruser'] = UserProfile.objects.get(user=self.request.user)
        return context
    
class TodoDelete(DeleteView):
    model = Todo
    success_url = reverse_lazy('todo_list')
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TodoDelete, self).dispatch(*args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super(TodoDelete, self).get_context_data(**kwargs)
        context['curruser'] = UserProfile.objects.get(user=self.request.user)
        return context

class Landing(TemplateView):
    template_name = "todos/landing.html"