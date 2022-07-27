from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, User


@receiver(post_save, sender=Post)
def notify_users_post(sender, instance, created, **kwargs):
    if created:
        subject = f'New post/article in you favorite category {instance.category}'
    else:
        subject = f'Post/article {instance.title} has been updated!'

    subscribers = instance.category.subscribers.all()
    address = []
    for a in subscribers:
        address.append(a.email)
    for user_id in list(instance.category.subscribers.all().values_list('subscriber', flat=True)):
        user = User.objects.get(id=user_id)
        html_content = render_to_string(
                                        'message_for_subscribers.html',
                                        {
                                            'text': instance.text,
                                            'title': instance.title,
                                            'category': instance.category,
                                            'username': user.username,
                                            'link': f'http://127.0.0.1:8000/Posts/{instance.id}',
                                        })
        msg = EmailMultiAlternatives(
            subject=subject,
            from_email='gregtmj@gmail.com',
            to=[*address],  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        msg.send()


def notify_post_create(sender, instance, **kwargs):
    subject = f'New post/article in you favorite category {instance.category}'
    subscribers = instance.category.subscribers.all()
    address = []
    for a in subscribers:
        address.append(a.email)

    for user_id in list(instance.category.subscribers.all().values_list('subscriber', flat=True)):
        user = User.objects.get(id=user_id)
        html_content = render_to_string(
                                        'message_for_subscribers.html',
                                        {
                                            'text': instance.text,
                                            'title': instance.title,
                                            'category': instance.category,
                                            'username': user.username,
                                            'link': f'http://127.0.0.1:8000/Posts/{instance.id}',
                                        })
        print(user.email)
        msg = EmailMultiAlternatives(
            subject=subject,
            from_email='gregtmj@gmail.com',
            to=[*address],  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        msg.send()


m2m_changed.connect(notify_post_create, sender=Post.category)
