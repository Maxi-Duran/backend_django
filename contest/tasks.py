from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def enviar_correo_ganador(name, email):
    """
    Envía un correo al ganador del concurso.
    """
    subject = "¡Felicidades! Has ganado"
    message = (
        f"Hola {name}, ¡felicidades! Has sido seleccionado como ganador del concurso. "
        f"Disfruta de tu estadía de 2 noches todo pagado en nuestro hotel."
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
    return f"Correo de ganador enviado a {email}"
