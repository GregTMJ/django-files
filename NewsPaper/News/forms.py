from django.forms import ModelForm, BooleanField
from .models import Posts


class PostForm(ModelForm):
    check_box = BooleanField(label="Don't forget to check")

    class Meta:
        model = Posts
        fields = [
            'Author',
            'title',
            'text',
            'category',
            'rating',
            'check_box',
        ]