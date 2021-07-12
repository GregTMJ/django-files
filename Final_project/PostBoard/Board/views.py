from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Post, Author, Category, Comments, User
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .forms import PostForm, EditForm, CommentForm, CommentEditForm
from .filters import SearchFilter


# Create your views here.

class Post_list(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'Post/list_of_posts.html'
    context_object_name = 'Posts'
    paginate_by = 5
    queryset = Post.objects.order_by('-id')


class Post_details(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'Post/post_details.html'
    context_object_name = 'Post'


class Post_create(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'Post/post_create.html'
    form_class = PostForm


class Post_update(LoginRequiredMixin, UpdateView):
    template_name = 'Post/post_update.html'
    form_class = EditForm
    context_object_name = 'Post'

    def get_object(self, **kwargs):
        # Here we are getting the id so Django could stalk the change
        ID = self.kwargs.get('pk')
        return Post.objects.get(pk=ID)


class Post_delete(LoginRequiredMixin, DeleteView):
    template_name = 'Post/post_delete.html'
    queryset = Post.objects.all()
    context_object_name = 'Post'
    success_url = '/Posts'


class Add_comment(LoginRequiredMixin, CreateView):
    model = Comments
    template_name = 'Post/add_comment.html'
    form_class = CommentForm
    success_url = '/Posts'

    def form_valid(self, form):
        form.instance.comment_id = self.kwargs['pk']
        return super().form_valid(form)


class List_of_Comments(LoginRequiredMixin, ListView):
    model = Comments
    template_name = 'Post/list_of_comments.html'
    context_object_name = 'comments'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        available_comments = Comments.objects.all()
        user = User.objects.get(id=self.request.user.id)
        context['filter'] = SearchFilter(self.request.GET,
                                         queryset=self.get_queryset())
        context['available_comments'] = available_comments
        context['author_id'] = user
        return context


class CommentEdit(LoginRequiredMixin, UpdateView):
    template_name = 'Post/edit_comment.html'
    form_class = CommentEditForm
    context_object_name = 'comments'

    def get_object(self, **kwargs):
        # Here we are getting the id so Django could stalk the change
        ID = self.kwargs.get('pk')
        return Comments.objects.get(pk=ID)


class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comments
    template_name = 'Post/comment_delete.html'
    queryset = Comments.objects.all()
    context_object_name = 'comments'
    success_url = '/Posts'


def AcceptedView(request, pk):
    comment = get_object_or_404(Comments, id=request.POST.get('comment.id'))

    if not comment.accepted:
        comment.accepted = True
    else:
        comment.accepted = False
    return HttpResponseRedirect(reverse('list_of_comments'))
