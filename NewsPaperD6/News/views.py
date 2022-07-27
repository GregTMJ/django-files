from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Author
from .forms import PostForm
from .filters import SearchFilter
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect


class Post_List(ListView):
    model = Post
    template_name = 'News/post_list.html'
    context_object_name = 'Posts'
    queryset = Post.objects.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class Post_detail(DetailView):
    model = Post
    template_name = 'News/post_details.html'
    context_object_name = 'Post'

    def get_context_data(self, **kwargs):
        context = super(Post_detail, self).get_context_data(**kwargs)
        mypost = get_object_or_404(Post, id=self.kwargs['pk'])
        category = mypost.category
        subscribed = False
        if category.subscribers.filter(id=self.request.user.id).exists():
            subscribed = True
        context['subscribed'] = subscribed
        return context


class PostCreate(CreateView, PermissionRequiredMixin):
    model = Post
    template_name = 'News/post_create.html'
    fields = '__all__'
    permission_required = ('News.add_posts',
                           'News.change_posts',
                           'News.delete_posts')

    """After we add a post, we search for subscribers of category """
    # An author cannot create more than 3 posts per day
    def form_valid(self, form):

        news_day_limit = 3
        author = Author.objects.get(author=self.request.user)
        form.instance.author = author

        if len(Post.objects.filter(author=author, time_in__date=datetime.today())) > news_day_limit:
            return redirect('/news/day_limit')

        else:
            return super().form_valid(form)

        # form.instance.created_by = self.request.user
        # subscribers = form.instance.category.subscribers.all()
        # instance = form.save()
        # address = []
        # for a in subscribers:
        #     address.append(a.email)
        # for user_id in list(subscribers.values_list('subscriber', flat=True)):
        #     user = User.objects.get(id=user_id)
        #
        #     html_content = render_to_string(
        #         'message_for_subscribers.html',
        #         {
        #             'text': form.instance.text,
        #             'title': form.instance.title,
        #             'category': form.instance.category,
        #             'username': user.username,
        #             'id': instance.id
        #         }
        #     )
        #     msg = EmailMultiAlternatives(
        #         subject=f'{form.instance.title}',
        #         body=form.instance.text,
        #         from_email='gregtmj@gmail.com',
        #         to=[*address],
        #     )
        #     msg.attach_alternative(html_content, "text/html")  # добавляем html
        #     msg.send()
        #     return super().form_valid(form)


class Search_List(ListView):
    model = Post
    template_name = 'News/search.html'
    context_object_name = 'search'
    form_class = PostForm
    ordering = ['-time_in']
    paginate_by = 10

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
    template_name = 'News/post_update.html'
    form_class = PostForm
    permission_required = 'News.change_posts'

    def get_object(self, **kwargs):
        post_pk = self.kwargs.get('pk')
        return Post.objects.get(pk=post_pk)


class PostDelete(DeleteView, PermissionRequiredMixin):
    template_name = 'News/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/Posts'
    permission_required = 'News.delete_posts'


# We give a user an opportunity to subscribe to a certain category
@login_required
def SubscribeView(request, pk):
    my_post = get_object_or_404(Post, id=pk)
    category = my_post.category
    if category.subscribers.filter(id=request.user.id).exists():
        category.subscribers.remove(request.user)
    else:
        category.subscribers.add(request.user)
    return HttpResponseRedirect(reverse('post_details', args=[str(pk)]))
