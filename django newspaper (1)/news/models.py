from django.db import models
from django.core.validators import MinValueValidator


class Post(models.Model):
    news = 'news'
    article = 'article'
    Posts = [(news, 'news'), (article, 'article'), ('select', 'select')]
    choosing = models.BooleanField(default=False)
    time_in = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, unique=True)
    text = models.CharField(max_length=255)
    rating = models.FloatField(default=0.0)

