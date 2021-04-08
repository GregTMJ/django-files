from datetime import date, datetime

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import SearchFilter
from .models import Posts
from .forms import PostForm
from django.core.paginator import Paginator



# Create your views here.


class Post_List(ListView):
    model = Posts
    template_name = 'post_list.html'
    context_object_name = 'Posts'
    queryset = Posts.objects.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now']= datetime.utcnow()
        return context


class Post_detail(DetailView):
    model = Posts
    template_name = 'post_details.html'
    context_object_name = 'Post'


class PostCreate(CreateView):
    template_name = 'post_create.html'
    form_class = PostForm


class Search_List(ListView):
    model = Posts
    template_name = 'search.html'
    context_object_name = 'search'
    form_class = PostForm
    ordering = ['-rating']
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = SearchFilter(self.request.GET,
                                         queryset=self.get_queryset())
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()

        return super().get(request, *args, **kwargs)


class PostUpdate(UpdateView):
    template_name = 'post_update.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Posts.objects.get(pk=id)


class PostDelete(DeleteView):
    template_name = 'post_delete.html'
    queryset = Posts.objects.all()
    success_url = '/Posts/<int:pk>'