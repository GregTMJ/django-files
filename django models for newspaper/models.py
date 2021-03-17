from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    def update_rating(self):
        author_post = Author.objects.filters(author=self.id)

        author_post_total_rating = 0
        for post in author_post:
            author_post_total_rating += post.post_rating * 3

        comments_author_rating = 0
        for comments in Comment.objects.fiters(user=self.author):
            comments_author_rating += comments.comment_rating

        post_total_rating = 0
        for _ in Post.objects.filters(post=author_post):
            post_total_rating += comments_author_rating

        self.author_rating = author_post_total_rating + \
                             comments_author_rating + \
                             post_total_rating

        self.save()


class Category(models.Model):
    category = models.CharField(max_length=255, unique=True, default='select category')

    def __str__(self):
        return self.category


class Post(models.Model):
    news = 'news'
    article = 'article'
    Posts = [(news, 'news'), (article, 'article'), ('select', 'select')]
    author = models.ForeignKey(Author, on_delete=models.CASCADE,
                               verbose_name='Author', blank=True,
                               null=True)
    post_type = models.CharField(max_length=30, choices=Posts,
                                 default='select', verbose_name='Type')
    post_choosing = models.BooleanField(default=False)
    post_time_in = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through='Choose post category')
    post_title = models.CharField(max_length=255, unique=True)
    post_text = models.CharField(max_length=255)
    post_rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.post_title

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def like(self):
        self.post_rating += 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post_commenting = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.CharField(default=255)
    time_comment = models.DateTimeField(auto_now_add=True)
    comment_rating = models.FloatField(default=0.0)

    def dislike(self):
        self.comment_rating -= 1
        self.save()

    def like(self):
        self.comment_rating += 1
        self.save()

    def __str__(self):
        return self.text_comment