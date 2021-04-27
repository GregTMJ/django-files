from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

# Create your views here.


class IndexView(TemplateView, LoginRequiredMixin):
    template_name = 'protect/Index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        premium_group.user_set.add(user)
    return redirect('/Posts/search')
