from datetime import timezone, datetime, timedelta
import time
from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Category, Post, Author

#
# @shared_task
# def Post_send(request, pk, **kwargs):
#     mypost = get_object_or_404(Post, id=pk)
#     category = mypost.category
#     if category.subscribers.filter(id=request.user.id).exists():
#         user = User.objects.get(id=request.user.id)
#         html_content = render_to_string(
#             'message_for_subscribers.html',
#             {
#                 'text': mypost.text,
#                 'title': mypost.title,
#                 'category': mypost.category,
#                 'username': user.username,
#                 'link': f'http://127.0.0.1:8000/Posts/{mypost.id}',
#             })
#         msg = EmailMultiAlternatives(
#             subject='New post in your favorite category',
#             from_email='gregtmj@gmail.com',
#             to=[user.email],  # это то же, что и recipients_list
#         )
#         msg.attach_alternative(html_content, "text/html")  # добавляем html
#         msg.send()


@shared_task
def weekly_posts():
    global Posts, subscriber, timing, cat
    timer = datetime.now(timezone.utc)

    Userposts = {
    }

    for cat in Category.objects.all():
        for subscriber in cat.subscribers.all():
            my_post = Post.objects.filter(category_id=cat.id, time_in__gte=(timer - timedelta(days=7)))
            Posts = list(my_post)
            if Posts:
                Userposts[subscriber] = Userposts.get(subscriber, []) + [Posts]
    Dict = Userposts.items()
    for user, art in Dict:
        html_content = render_to_string(
            'weekly_message_for_subscribers.html',
            {
                'user': user,
                'art': art,
            }
        )
        msg = EmailMultiAlternatives(
            subject='Weekly posts',
            from_email='gregtmj@gmail.com',
            to=[user.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
