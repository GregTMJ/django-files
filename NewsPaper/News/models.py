from django.db import models


# Create your models here.


class Posts(models.Model):

    Author = models.CharField(max_length=100,
                              default='Author')
    title = models.CharField(max_length=50,
                             default='Some article',
                             unique=True, )
    text = models.TextField(max_length=255)
    time_in = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0.0)
    choosing = models.BooleanField(default=False)
    category = models.CharField(max_length=100,
                                unique=True)

    def __str__(self):
        return f'{self.title}: {self.text[:50]}'
    
    def get_absolute_url(self):
        return f'/Posts/{self.id}'

