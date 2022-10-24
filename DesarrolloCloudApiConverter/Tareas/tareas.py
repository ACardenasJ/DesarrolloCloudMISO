from celery import Celery
import requests
from time import sleep

celery = Celery(__name__, broker='redis://redis:6379/0')

def reintegrar_cola(str_data):
    #AGREGA A LA COLA DE TAREAS
    args = (str_data,)
    escribir_cola.apply_async(args = args)


@celery.task(name="escribir_cola")
def escribir_cola(data):
    #print(data)
    
    # with open('log_registrar_info.txt','a+') as file:
    #     file.write('{}\n'.format(data))

    try:
        rslt = requests.get('http://converter:5002/api/status')
        #print(rslt)
        if rslt.status_code == 200:
            requests.post('http://converter:5002/api/convertidor', json=data)
        else:
            reintegrar_cola(data)
    except requests.exceptions.ConnectionError as r:
        r.status_code = "Connection refused"
        print(r.status_code)
        print(r)
        reintegrar_cola(data)
        sleep(2)

