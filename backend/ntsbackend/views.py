from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
# Create your views here.
from .forms import TextForm
from .Functions import GetData


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TextForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # From this we get the result of POST method
            date = form.cleaned_data['date']
            splitdate = date.split(sep='-')
            # Here we call the class created in Functions.py
            x = GetData(int(splitdate[2]), int(splitdate[1]), int(splitdate[0]))
            x.getInfo()
            context = {
                'text': date,
                'form': form,
            }
            return render(request, 'index.html', context)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = TextForm()
    return render(request, 'index.html', {'form': form})
