from django.db import models
from django.contrib.auth.models import User


# Instead of using just a field for the author, knowing that the author is a user
class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author}'


# Many posts can have the same category, that's why we use for it a independent model
class Category(models.Model):
    category = models.CharField(max_length=255, unique=True, default='select category')
    subscribers = models.ManyToManyField(User, related_name='subscriber')

    def __str__(self):
        return self.category


class Post(models.Model):
    news = 'news'
    article = 'article'
    Posts = [(news, 'news'), (article, 'article'), ('select', 'select')]
    author = models.ForeignKey(Author, on_delete=models.CASCADE,
                               verbose_name='User', blank=True,
                               null=True)
    choosing = models.BooleanField(default=False)
    time_in = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True)
    text = models.TextField(max_length=255)
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return f'{self.title}: {self.text[:50]}'

    def get_absolute_url(self):
        return f'/Posts/{self.pk}'
