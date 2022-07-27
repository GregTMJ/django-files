from datetime import timezone, datetime, timedelta
from celery import shared_task
from .models import Category, Post, User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


# For each new created post, we need to send a notification
@shared_task
def Post_send(oid, **kwargs):
    post = Post.objects.get(pk=oid)
    post_subscribers = post.category.subscribers.all()
    address = []
    for a in post_subscribers:
        address.append(a.email)
    for user_id in list(post.category.subscribers.all().values_list('subscriber', flat=True)):
        user = User.objects.get(id=user_id)
        html_content = render_to_string(
            'message_for_subscribers.html',
            {
                'text': post.text,
                'title': post.title,
                'category': post.category,
                'username': user.username,
                'link': f'http://127.0.0.1:8000/Posts/{post.id}',
            })
        msg = EmailMultiAlternatives(
            subject='New post coming to you',
            from_email='gregtmj@gmail.com',
            to=[*address],  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        msg.send()


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
