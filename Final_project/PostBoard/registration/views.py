from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.models import Group


# Create your views here.

class BaseView(TemplateView):
    template_name = 'base.html'