from django.urls import path
from .views import Post_list, Post_create, Post_delete, Post_details, Post_update, \
    Add_comment, CommentEdit, CommentDelete, List_of_Comments, AcceptedView
from django.views.generic import TemplateView

urlpatterns = [
    path('', Post_list.as_view()),
    path('<int:pk>', Post_details.as_view(), name='post_details'),
    path('add/', Post_create.as_view(), name='post_create'),
    path('<int:pk>/edit/', Post_update.as_view(), name='post_update'),
    path('<int:pk>/delete/', Post_delete.as_view(), name='post_delete'),
    path('<int:pk>/comment/', Add_comment.as_view(), name='add_comment'),
    path('comment/<int:pk>/edit/', CommentEdit.as_view(), name='edit_comment'),
    path('comment/<int:pk>/delete/', CommentDelete.as_view(), name='delete_comment'),
    path('list_of_comments/', List_of_Comments.as_view(), name='list_of_comments'),
    path('Accepted/<int:pk>', AcceptedView, name='accepted'),
]