from allauth.socialaccount.forms import SignupForm
from django.contrib.auth.models import Group
from django.forms import ModelForm, BooleanField
from .models import Post


class PostForm(ModelForm):
    check_box = BooleanField(label="Don't forget to check")

    class Meta:
        model = Post
        fields = [
            'author',
            'title',
            'text',
            'category',
            'rating',
            'check_box',
        ]

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


