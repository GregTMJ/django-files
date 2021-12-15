from django import forms


class TextForm(forms.Form):
    date = forms.CharField(widget=forms.TextInput(attrs={'type': 'date'}), label=False)
