from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import SearchFilter
from .models import Posts
from .forms import PostForm

"""
If we want to use the details of a model, or use a certain parameter, we should use the get_context_data, to give the 
templates the context 
"""


# Here we are just listing all available posts in a post_list.html
class Post_List(ListView):
    model = Posts
    template_name = 'post_list.html'
    context_object_name = 'Posts'
    # Order by id desc
    queryset = Posts.objects.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


# Shows the details of a certain post (fields show) in post_details.html
class Post_detail(DetailView):
    model = Posts
    template_name = 'post_details.html'
    context_object_name = 'Post'


# Creates a post by a certain user
class PostCreate(CreateView):
    template_name = 'post_create.html'
    form_class = PostForm


# Add the possibility to search for a concrete post
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


# By giving to slug(pk) of a post, we can update the information
class PostUpdate(UpdateView):
    template_name = 'post_update.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        # Important! never use a variable that is already in the query of django, example:
        # id = self.kwargs.get('pk') - id is already defined by django
        post_pk = self.kwargs.get('pk')
        return Posts.objects.get(pk=post_pk)


# Deletes the post by pk
class PostDelete(DeleteView):
    template_name = 'post_delete.html'
    queryset = Posts.objects.all()
    success_url = '/Posts/<int:pk>'
