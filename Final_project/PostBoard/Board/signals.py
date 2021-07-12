from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect
from django.template.loader import render_to_string
from .models import Post, User, Comments


@receiver(post_save, sender=Comments)
def notify_users_post(sender, instance, created, **kwargs):
    if created:
        subject = f'{instance.name} has just commented on your post'

    post_id = instance.post.id
    post = Post.objects.get(id=post_id)
    username = instance.username
    email = post.author.email
    html_content = render_to_string(
                                        'message_for_subscribers.html',
                                        {
                                            'name': instance.name,
                                            'text': instance.text,
                                            'category': instance.post.cat,
                                            'username': username,
                                            'link': f'http://127.0.0.1:8000/Posts/list_of_comments/',
                                        })
    msg = EmailMultiAlternatives(
            subject=subject,
            from_email='gregtmj@gmail.com',
            to=email,
        )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return redirect('/Posts')


def notify_post_create(sender, instance, **kwargs):
    subject = f'{instance.name} has just commented on your post'
    post_id = instance.post.id
    post = Post.objects.get(id=post_id)
    username = instance.username
    email = post.author.email
    html_content = render_to_string(
        'message_for_subscribers.html',
        {
            'name': instance.name,
            'text': instance.text,
            'category': instance.post.cat,
            'username': username,
            'link': f'http://127.0.0.1:8000/Posts/list_of_comments/',
        })
    msg = EmailMultiAlternatives(
        subject=subject,
        from_email='gregtmj@gmail.com',
        to=email,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


m2m_changed.connect(notify_post_create, sender=Comments)


@receiver(post_save, sender=Comments)
def notify_Commentor(instance, sender, **kwargs):
    subject = f'Your post is ready to be read'
    comment_id = instance.id
    user_comment = Comments.objects.get(id=comment_id)
    name = user_comment.username
    user_comment_email = user_comment.username.email
    post_id = user_comment.post.id
    if user_comment.accepted:
        html_content = render_to_string(
            'message_for_commentator.html',
            {
                'name': instance.name,
                'post': instance.post,
                'text': instance.text,
                'category': instance.post.cat,
                'username': name,
                'link': f'http://127.0.0.1:8000/Posts/{post_id} ',
            })
        msg = EmailMultiAlternatives(
            subject=subject,
            from_email='gregtmj@gmail.com',
            to=user_comment_email,
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return redirect('/Posts')

