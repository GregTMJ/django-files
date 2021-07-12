from django import forms
from .models import Post, Comments
from ckeditor.fields import RichTextField


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'author', 'cat', 'body', 'image')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'cat': forms.Select(attrs={'class': 'form-control'}),
            'body': forms.TextInput(attrs={'class': 'form-control'}),
        }


class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'cat', 'body')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'cat': forms.Select(attrs={'class': 'form-control'}),
            'body': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('post', 'name', 'username', 'text')

        widgets = {
            'post': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'username': forms.Select(attrs={'class': 'form-control'}),
        }


class CommentEditForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)

        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'}),
        }
