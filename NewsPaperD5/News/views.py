from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .filters import SearchFilter
from .models import Posts
from .forms import PostForm
from django.contrib.auth.mixins import PermissionRequiredMixin


class Post_List(ListView):
    model = Posts
    template_name = 'post_list.html'
    context_object_name = 'Posts'
    queryset = Posts.objects.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


# a Permission Required Mixin is required, which means the admin must give you a status, that will give you access
class Post_detail(DetailView, PermissionRequiredMixin):
    model = Posts
    template_name = 'post_details.html'
    context_object_name = 'Post'
    permission_required = 'News.view_posts'


class PostCreate(CreateView, PermissionRequiredMixin):
    template_name = 'post_create.html'
    form_class = PostForm
    permission_required = 'News.add_posts'


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


class PostUpdate(UpdateView, PermissionRequiredMixin):
    template_name = 'post_update.html'
    form_class = PostForm
    permission_required = 'News.change_posts'

    def get_object(self, **kwargs):
        post_pk = self.kwargs.get('pk')
        return Posts.objects.get(pk=post_pk)


class PostDelete(DeleteView, PermissionRequiredMixin):
    template_name = 'post_delete.html'
    queryset = Posts.objects.all()
    success_url = '/Posts/<int:pk>'
    permission_required = 'News.delete_posts'
