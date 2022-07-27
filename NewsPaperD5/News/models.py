"""
The same models as NewsPaper project + basic signup model
"""
from django.db import models
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

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
        return f'/Posts/{self.pk}'


# Django provides us a class, that has already the required fields for a signup
class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
