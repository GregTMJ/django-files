from django.urls import path
from .views import Post_List, Post_detail, Search_List, PostCreate, PostDelete, PostUpdate, SubscribeView
from django.views.generic import TemplateView

urlpatterns = [
    path('', Post_List.as_view()),
    path('<int:pk>', Post_detail.as_view(), name='post_details'),
    path('search/', Search_List.as_view(), name='search'),
    path('add/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('<int:pk>/edit', PostUpdate.as_view(), name='post_update'),
    path('subscribe/<int:pk>', SubscribeView, name='subscribe'),
    path('day_limit/', TemplateView.as_view(template_name='Post_limit_PerDay.html')),
]
