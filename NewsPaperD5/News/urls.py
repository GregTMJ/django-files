from django.urls import path
from .views import Post_List, Post_detail, Search_List, PostCreate, PostDelete, PostUpdate

urlpatterns = [
    path('', Post_List.as_view()),
    path('<int:pk>', Post_detail.as_view(), name='post_details'),
    path('search/', Search_List.as_view(), name='search'),
    path('add/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('<int:pk>/edit', PostUpdate.as_view(), name='post_update'),

]
