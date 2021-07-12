from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


# Create your models here.


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author}'


class Category(models.Model):
    category = models.CharField(max_length=255,
                                unique=True,
                                default='')

    def __str__(self):
        return f'{self.category}'


class Post(models.Model):
    author = models.OneToOneField(Author,
                                  blank=True,
                                  null=True,
                                  on_delete=models.CASCADE)
    title = models.CharField(max_length=255,
                             unique=True,
                             default='random')
    cat = models.ForeignKey(Category,
                            on_delete=models.CASCADE)
    body = RichTextField(blank=True, null=True)
    time_in = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/')

    def __str__(self):
        return f"{self.title}: {self.body[0:10]}"

    def get_absolute_url(self):
        return f'/Posts/{self.pk}'


class Comments(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    text = models.TextField(default='')
    date_added = models.DateTimeField(auto_now_add=True)
    username = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.post.title}-{self.name}-{self.text}"

    def get_absolute_url(self):
        return f'/Posts/'
