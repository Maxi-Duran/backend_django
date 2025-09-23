from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def enviar_correo_verificacion(name, email, verification_link):
    send_mail(
        subject='Verifica tu correo',
        message=f'Hola {name}, por favor verifica tu correo haciendo clic en este enlace: {verification_link}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
