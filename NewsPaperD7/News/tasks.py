"""
Here we are getting the weekly posts for certain categories and send them the subscribers
"""
from datetime import timezone, datetime, timedelta
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Category, Post


# shared_task is used to make celery identify
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
