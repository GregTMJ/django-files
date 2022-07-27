from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.db import models

# Create your models here.


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
