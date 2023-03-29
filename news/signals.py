from allauth.account.signals import email_confirmed
from django.core.mail import send_mail, mail_managers
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from .models import Appointment
from .models import Post


@receiver(email_confirmed)
def user_signed_up(request, email_address, **kwargs):
    send_mail(
        subject=f'Dear {email_address.user} Welcome to News Portal!',
        message=f'Приветствую Вас на моём новостном портале. Здесь самые последние новости из разных категорий',
        from_email='defferius@yandex.ru',
        recipient_list=[email_address.user.email]
    )


@receiver(m2m_changed, sender=Post.categories.through)
def new_post(sender, action, instance, **kwargs):
    if action == 'post_add':
        for each in instance.categories.all():
            for cat in each.subscribers.all():
                send_mail(
                    subject=f'Выложен новый пост "{instance.headline}"!',
                    message=f'Привет, {cat}! На новостном портале новый пост по твоей подписке'
                            f' - "{instance.content[:30]}", '
                            f'переходи по ссылке - http://127.0.0.1:8000/news/{instance.id}',
                    from_email='defferius@yandex.ru',
                    recipient_list=[cat.email]
                )


@receiver(post_save, sender=Appointment)
def notify_managers_appointment(sender, instance, created, **kwargs):
    if created:
        subject = f'{instance.client_name} {instance.date.strftime("%d %m %Y")}'
    else:
        subject = f'Appointment changed for {instance.client_name} {instance.date.strftime("%d %m %Y")}'

    mail_managers(
        subject=subject,
        message=instance.message,
    )
