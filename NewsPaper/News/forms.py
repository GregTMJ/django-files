from django.forms import ModelForm, BooleanField
from .models import Posts


# The form to a post or update is defined here by fields
# Plus we can add some validation or whatever feature you like to add
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