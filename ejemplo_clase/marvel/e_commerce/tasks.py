from marvel.settings import VERDE
from celery import shared_task
from e_commerce.communications import SendCommunication


@shared_task
def hello_world():
    print(VERDE+'Hola mundo celery!!!')

@shared_task
def segunda_tarea():
    SendCommunication.send_mail(
        subject='Prueba Nueva',
        message='Prueba',
        recipient_list=['emmaotm@gmail.com'],
    )
    print(VERDE+'Segunda tarea!!!')
