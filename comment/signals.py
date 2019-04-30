import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings
from notifications.signals import notify
from .models import Comment
from django.urls import reverse


@receiver(post_save, sender=Comment)
def send_notification(sender, instance, **kwargs):
    # 发送站内消息
    recipient = instance.article.author
    article = instance.article
    print(instance.author.username, article)
    verb = instance.content
    notify.send(instance.author, recipient=recipient, verb=verb, action_object=instance,
                author_=instance.author.username, author_url=reverse('user_home', kwargs={'user_name':instance.author.username}),
                title_=article.title, article_url=reverse('article_detail', kwargs={'article_id': article.pk}) + "#comment_" + str(instance.pk),
                )


class SendMail(threading.Thread):
    def __init__(self, subject, text, email, fail_silently=False):
        self.subject = subject
        self.text = text
        self.email = email
        self.fail_silently = fail_silently
        threading.Thread.__init__(self)

    def run(self):
        send_mail(
            self.subject,
            '',
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently=self.fail_silently,
            html_message=self.text
        )
