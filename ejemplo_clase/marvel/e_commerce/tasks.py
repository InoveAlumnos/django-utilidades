from marvel.settings import VERDE
from celery import shared_task
from e_commerce.communications import SendCommunication


@shared_task
def hello_world_task():
    print(VERDE+'Hola mundo celery!!!')


@shared_task
def periodic_send_email_task():
    SendCommunication.send_email(
        subject='Envío de Email Periódico',
        message=(
            'Este email se envía utilizando Celery Beat de manera periódica.'
        ),
        recipient_list=['emmaotm+5@gmail.com'],
    )
    print(VERDE+'Acaba de enviarse un email!!!')


@shared_task
def send_email_auth_task(subject, message, receiver):
    SendCommunication.send_email(
        subject=subject,
        message=message,
        recipient_list=[receiver]
    )
