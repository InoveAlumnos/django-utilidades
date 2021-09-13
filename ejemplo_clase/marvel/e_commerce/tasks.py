from marvel.settings import VERDE
from celery import shared_task
from tools.gmail import Gmail


@shared_task
def hello_world():
    print(VERDE+'Hola mundo celery!!!')

@shared_task
def segunda_tarea():
    gmail = Gmail("./tools/client_secret.json")
    gmail.send_mail("Probando", "mi mensaje", ["hhvservice@gmail.com"])
    print(VERDE+'Segunda tarea!!!')
