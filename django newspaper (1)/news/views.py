from django.shortcuts import render

# Create your views here.
from django.views.generic import \
    ListView, DetailView  # импортируем класс, который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
from .models import Post
import datetime


class Postlist(ListView):
    model = Post
    # указываем модель, объекты которой мы будем выводить
    template_name = 'Post.html'  # указываем имя шаблона, в котором будет лежать html, в котором будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'posts'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через html-шаблон
    queryset = Post.objects.order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.datetime.utcnow()  # добавим переменную текущей даты time_now
        return context


class PostDetail(DetailView):
    model = Post # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    template_name = 'posts.html' # название шаблона будет product.html
    context_object_name = 'posts'  # название объекта. в нём будет

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.datetime.utcnow()  # добавим переменную текущей даты time_now
        return context